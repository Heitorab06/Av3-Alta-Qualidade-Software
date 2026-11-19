"""Carrinho de compras responsável pelo armazenamento e consolidação de itens."""

import logging
from collections.abc import Mapping

from catalog import CatalogReader
from model_objects import Discount, Offer, Product, ProductQuantity, ProductUnit
from offers import (
    OfferFactory,
    OfferStrategy,
    calculate_legacy_discount,
    is_strategy_offers_enabled,
    to_legacy_offer,
)
from receipt import Receipt

logger = logging.getLogger(__name__)


class ShoppingCart:
    """Carrinho de compras do cliente.

    Mantém o histórico de adições e as quantidades consolidadas por produto (SRP).
    """

    def __init__(self) -> None:
        """Inicializa o carrinho vazio."""
        self._items: list[ProductQuantity] = []
        self._product_quantities: dict[Product, float] = {}

    @property
    def items(self) -> list[ProductQuantity]:
        """Lista com cada registro de adição de item (cópia defensiva)."""
        return self._items[:]

    def add_item(self, product: Product) -> None:
        """Adiciona 1 unidade do produto ao carrinho."""
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self) -> dict[Product, float]:
        """Dicionário consolidado com {produto: quantidade_total} (cópia defensiva)."""
        return self._product_quantities.copy()

    def add_item_quantity(self, product: Product, quantity: float) -> None:
        """Adiciona uma quantidade do produto ao carrinho validando invariantes."""
        if quantity <= 0.0:
            raise ValueError(
                "A quantidade adicionada deve ser maior que zero (INV-04)."
            )
        if product.unit == ProductUnit.EACH and not float(quantity).is_integer():
            raise ValueError(
                "Produtos vendidos por unidade (EACH) exigem quantidades inteiras "
                "(INV-05)."
            )

        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities:
            self._product_quantities[product] += quantity
        else:
            self._product_quantities[product] = quantity

    def handle_offers(
        self,
        receipt: Receipt,
        offers: Mapping[Product, OfferStrategy | Offer],
        catalog: CatalogReader,
    ) -> None:
        """Delega o cálculo de descontos às estratégias com fallback legado (Nível 1).

        Respeita a feature toggle ENABLE_STRATEGY_OFFERS e realiza comutação
        automática para o motor legado em caso de exceção ou inconsistência.
        """
        offer_factory = OfferFactory()
        use_strategy = is_strategy_offers_enabled()
        for product, quantity in self._product_quantities.items():
            if product not in offers:
                continue

            offer = offers[product]
            unit_price = catalog.unit_price(product)
            discount = self._calculate_offer_discount(
                product, quantity, unit_price, offer, offer_factory, use_strategy
            )
            if discount is not None:
                receipt.add_discount(discount)

    def _calculate_offer_discount(
        self,
        product: Product,
        quantity: float,
        unit_price: float,
        offer: OfferStrategy | Offer,
        offer_factory: OfferFactory,
        use_strategy: bool,
    ) -> Discount | None:
        """Calcula o desconto pelo motor ativo, acionando fallback legado se falhar."""
        if not use_strategy:
            return self._calculate_with_legacy_fallback(
                product, quantity, unit_price, offer
            )

        try:
            strategy = (
                offer
                if isinstance(offer, OfferStrategy)
                else offer_factory.create_offer(offer.offer_type, offer.argument)
            )
            discount = strategy.calculate_discount(product, quantity, unit_price)
            gross_total = unit_price * quantity
            if (
                discount is not None
                and abs(discount.discount_amount) > gross_total + 1e-9
            ):
                raise ValueError("Desconto excede o valor bruto do item (INV-03).")
            return discount
        except Exception:
            logger.warning(
                "Falha no motor de estratégias para '%s'; comutando para motor legado.",
                product.name,
            )
            return self._calculate_with_legacy_fallback(
                product, quantity, unit_price, offer
            )

    @staticmethod
    def _calculate_with_legacy_fallback(
        product: Product,
        quantity: float,
        unit_price: float,
        offer: OfferStrategy | Offer,
    ) -> Discount | None:
        """Executa o motor legado quando há equivalente de oferta suportado."""
        legacy_offer = to_legacy_offer(product, offer)
        if legacy_offer is None:
            return None
        return calculate_legacy_discount(product, quantity, unit_price, legacy_offer)
