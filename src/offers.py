"""Módulo de estratégias de cálculo de ofertas (Strategy) e fábrica de promoções (Factory Method)."""

from abc import ABC, abstractmethod
from typing import Optional, Union

from model_objects import Discount, Product, SpecialOfferType


class OfferStrategy(ABC):
    """
    Interface Strategy para cálculo de descontos promocionais (OCP / SRP).
    Novas promoções podem ser adicionadas criando novas subclasses sem alterar o carrinho ou o caixa.
    """

    @abstractmethod
    def calculate_discount(
        self, product: Product, quantity: float, unit_price: float
    ) -> Optional[Discount]:
        """Calcula e retorna um objeto Discount se aplicável, ou None caso contrário."""


class ThreeForTwoStrategy(OfferStrategy):
    """Estratégia para a promoção 'Leve 3, Pague 2' (não exige parâmetros extras)."""

    def calculate_discount(
        self, product: Product, quantity: float, unit_price: float
    ) -> Optional[Discount]:
        """Calcula o desconto de 1 unidade gratuita a cada grupo de 3 unidades."""
        quantity_as_int = int(quantity)
        if quantity_as_int < 3:
            return None

        number_of_packs = quantity_as_int // 3
        remainder = quantity_as_int % 3
        total_with_discount = (number_of_packs * 2 * unit_price) + (remainder * unit_price)
        discount_amount = (quantity * unit_price) - total_with_discount
        return Discount(product, "3 for 2", -discount_amount)


class PercentageDiscountStrategy(OfferStrategy):
    """Estratégia para desconto percentual direto sobre o valor total do item."""

    def __init__(self, percent: float) -> None:
        """Inicializa a estratégia com o percentual de desconto a ser aplicado."""
        self.percent: float = percent

    def calculate_discount(
        self, product: Product, quantity: float, unit_price: float
    ) -> Optional[Discount]:
        """Calcula o abatimento percentual sobre o preço total da quantidade comprada."""
        discount_amount = quantity * unit_price * (self.percent / 100.0)
        return Discount(product, f"{self.percent}% off", -discount_amount)


class AmountForQuantityStrategy(OfferStrategy):
    """Estratégia para promoções do tipo 'Leve N unidades por um valor fixo' (ex: 2 por X, 5 por Y)."""

    def __init__(self, required_quantity: int, amount: float) -> None:
        """Inicializa a estratégia com a quantidade exigida por pacote e o preço promocional do pacote."""
        self.required_quantity: int = required_quantity
        self.amount: float = amount

    def calculate_discount(
        self, product: Product, quantity: float, unit_price: float
    ) -> Optional[Discount]:
        """Calcula o desconto para pacotes fechados de N unidades pelo valor promocional."""
        quantity_as_int = int(quantity)
        if quantity_as_int < self.required_quantity:
            return None

        number_of_packs = quantity_as_int // self.required_quantity
        remainder = quantity_as_int % self.required_quantity
        total_with_discount = (self.amount * number_of_packs) + (remainder * unit_price)
        discount_amount = (unit_price * quantity) - total_with_discount
        return Discount(product, f"{self.required_quantity} for {self.amount}", -discount_amount)


class OfferFactory:
    """
    Padrão Factory Method para criação de estratégias de oferta (OfferStrategy).
    Isola a lógica de instanciação das promoções concretas.
    """

    def create_offer(
        self,
        offer_type: Union[SpecialOfferType, OfferStrategy],
        argument: Optional[float] = None,
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
