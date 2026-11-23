"""Estratégias de cálculo de ofertas (Strategy) e fábrica (Factory Method)."""

import os
from abc import ABC, abstractmethod
from collections.abc import Mapping

from catalog import CatalogReader
from model_objects import Discount, Offer, Product, ProductUnit, SpecialOfferType

_FALSY_VALUES = {"false", "0", "no", "off"}
_TRUTHY_VALUES = {"true", "1", "yes", "on"}


def is_strategy_offers_enabled() -> bool:
    """Indica se o motor de ofertas por Strategy está ativo via variável de ambiente."""
    raw = os.getenv("ENABLE_STRATEGY_OFFERS", "true").strip().lower()
    return raw not in _FALSY_VALUES


def is_pdv_emergency_mode() -> bool:
    """Indica se o modo de emergência manual do PDV está ativo via ambiente."""
    raw = os.getenv("PDV_EMERGENCY_MODE", "false").strip().lower()
    return raw in _TRUTHY_VALUES


class OfferStrategy(ABC):
    """Interface Strategy para cálculo de descontos promocionais (OCP / SRP).

    Novas promoções podem ser adicionadas criando novas subclasses sem alterar
    o carrinho ou o caixa.
    """

    @abstractmethod
    def calculate_discount(
        self, product: Product, quantity: float, unit_price: float
    ) -> Discount | None:
        """Calcula e retorna um Discount se aplicável, ou None caso contrário."""


class ThreeForTwoStrategy(OfferStrategy):
    """Estratégia para a promoção 'Leve 3, Pague 2' (sem parâmetros extras)."""

    def calculate_discount(
        self, product: Product, quantity: float, unit_price: float
    ) -> Discount | None:
        """Calcula o desconto de 1 unidade gratuita a cada grupo de 3 unidades."""
        quantity_as_int = int(quantity)
        if quantity_as_int < 3:
            return None

        number_of_packs = quantity_as_int // 3
        remainder = quantity_as_int % 3
        total_with_discount = (number_of_packs * 2 * unit_price) + (
            remainder * unit_price
        )
        discount_amount = (quantity * unit_price) - total_with_discount
        return Discount(product, "3 for 2", -discount_amount)


class PercentageDiscountStrategy(OfferStrategy):
    """Estratégia para desconto percentual direto sobre o valor total do item."""

    def __init__(self, percent: float) -> None:
        """Inicializa a estratégia com o percentual de desconto (entre 0 e 100)."""
        if percent < 0.0 or percent > 100.0:
            raise ValueError(
                "O percentual de desconto deve estar entre 0 e 100 (INV-03)."
            )
        self.percent: float = percent

    def calculate_discount(
        self, product: Product, quantity: float, unit_price: float
    ) -> Discount | None:
        """Calcula o abatimento percentual sobre o valor bruto do item."""
        discount_amount = quantity * unit_price * (self.percent / 100.0)
        return Discount(product, f"{self.percent}% off", -discount_amount)


class AmountForQuantityStrategy(OfferStrategy):
    """Estratégia para promoções 'Leve N unidades por valor fixo' (2 por X, 5 por Y)."""

    def __init__(self, required_quantity: int, amount: float) -> None:
        """Inicializa a estratégia com a quantidade e o valor promocional do pacote."""
        if required_quantity <= 0 or amount < 0.0:
            raise ValueError(
                "Quantidade do pacote deve ser positiva e valor não negativo (INV-04)."
            )
        self.required_quantity: int = required_quantity
        self.amount: float = amount

    def calculate_discount(
        self, product: Product, quantity: float, unit_price: float
    ) -> Discount | None:
        """Calcula o desconto para pacotes fechados de N unidades pelo valor fixo."""
        quantity_as_int = int(quantity)
        if quantity_as_int < self.required_quantity:
            return None

        number_of_packs = quantity_as_int // self.required_quantity
        remainder = quantity_as_int % self.required_quantity
        total_with_discount = (self.amount * number_of_packs) + (remainder * unit_price)
        gross_total = unit_price * quantity
        discount_amount = min(gross_total - total_with_discount, gross_total)
        return Discount(
            product,
            f"{self.required_quantity} for {self.amount}",
            -discount_amount,
        )


class ComboOffer:
    """Estratégia de promoção de combo aplicada a um conjunto de produtos."""

    def __init__(
        self,
        required_items: Mapping[Product, float],
        discount_percent: float,
    ) -> None:
        """Inicializa o combo com os produtos exigidos e o percentual de desconto."""
        if not required_items or any(
            quantity <= 0.0 for quantity in required_items.values()
        ):
            raise ValueError(
                "O combo deve conter itens com quantidades maiores que zero (INV-04)."
            )
        if discount_percent < 0.0 or discount_percent > 100.0:
            raise ValueError(
                "O percentual de desconto deve estar entre 0 e 100 (INV-03)."
            )
        self.required_items: dict[Product, float] = dict(required_items)
        self.discount_percent: float = discount_percent

    def calculate_discount(
        self,
        available_quantities: dict[Product, float],
        catalog: CatalogReader,
    ) -> Discount | None:
        """Calcula o desconto de combos completos e consome os itens utilizados."""
        combo_count = min(
            int(available_quantities.get(product, 0.0) // required_qty)
            for product, required_qty in self.required_items.items()
        )
        if combo_count <= 0:
            return None

        combo_unit_price = sum(
            catalog.unit_price(product) * required_qty
            for product, required_qty in self.required_items.items()
        )
        discount_amount = (
            combo_count * combo_unit_price * (self.discount_percent / 100.0)
        )

        for product, required_qty in self.required_items.items():
            available_quantities[product] -= combo_count * required_qty

        return Discount(
            Product("combo", ProductUnit.EACH),
            f"{self.discount_percent}% off",
            -discount_amount,
        )


def to_legacy_offer(product: Product, offer: OfferStrategy | Offer) -> Offer | None:
    """Retorna um Offer legado equivalente à estratégia para fallback (Nível 1)."""
    if isinstance(offer, Offer):
        return offer
    if isinstance(offer, ThreeForTwoStrategy):
        return Offer(SpecialOfferType.THREE_FOR_TWO, product, None)
    if isinstance(offer, PercentageDiscountStrategy):
        return Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, product, offer.percent)
    if isinstance(offer, AmountForQuantityStrategy):
        if offer.required_quantity == 2:
            return Offer(SpecialOfferType.TWO_FOR_AMOUNT, product, offer.amount)
        if offer.required_quantity == 5:
            return Offer(SpecialOfferType.FIVE_FOR_AMOUNT, product, offer.amount)
    return None


def calculate_legacy_discount(
    product: Product, quantity: float, unit_price: float, offer: Offer
) -> Discount | None:
    """Motor legado de cálculo de ofertas usado em fallback/feature toggle (Nível 1)."""
    quantity_as_int = int(quantity)
    if offer.offer_type == SpecialOfferType.THREE_FOR_TWO and quantity_as_int >= 3:
        packs = quantity_as_int // 3
        remainder = quantity_as_int % 3
        discount_amount = (quantity * unit_price) - (
            packs * 2 * unit_price + remainder * unit_price
        )
        return Discount(product, "3 for 2", -discount_amount)

    if (
        offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT
        and offer.argument is not None
    ):
        discount_amount = quantity * unit_price * offer.argument / 100.0
        return Discount(product, f"{offer.argument}% off", -discount_amount)

    if (
        offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT
        and offer.argument is not None
        and quantity_as_int >= 2
    ):
        packs = quantity_as_int // 2
        remainder = quantity_as_int % 2
        total = offer.argument * packs + remainder * unit_price
        discount_amount = (unit_price * quantity) - total
        return Discount(product, f"2 for {offer.argument}", -discount_amount)

    if (
        offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT
        and offer.argument is not None
        and quantity_as_int >= 5
    ):
        packs = quantity_as_int // 5
        remainder = quantity_as_int % 5
        total = offer.argument * packs + remainder * unit_price
        discount_amount = (unit_price * quantity) - total
        return Discount(product, f"5 for {offer.argument}", -discount_amount)

    return None


class OfferFactory:
    """Fábrica (Factory Method) para criação de estratégias de oferta.

    Isola a lógica de instanciação das promoções concretas.
    """

    def create_offer(
        self,
        offer_type: SpecialOfferType | OfferStrategy,
        argument: float | None = None,
    ) -> OfferStrategy:
        """Retorna a estratégia de oferta correspondente ao tipo informado."""
        if isinstance(offer_type, OfferStrategy):
            return offer_type
        if offer_type == SpecialOfferType.THREE_FOR_TWO:
            return ThreeForTwoStrategy()
        if offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT and argument is not None:
            return PercentageDiscountStrategy(argument)
        if offer_type == SpecialOfferType.TWO_FOR_AMOUNT and argument is not None:
            return AmountForQuantityStrategy(2, argument)
        if offer_type == SpecialOfferType.FIVE_FOR_AMOUNT and argument is not None:
            return AmountForQuantityStrategy(5, argument)
        raise ValueError(f"Tipo de oferta não suportado: {offer_type}")
