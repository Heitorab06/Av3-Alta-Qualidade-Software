"""Módulo do carrinho de compras responsável pelo armazenamento e consolidação de itens."""

from typing import Union

from catalog import CatalogReader
from model_objects import Offer, Product, ProductQuantity
from offers import OfferFactory, OfferStrategy
from receipt import Receipt


class ShoppingCart:
    """
    Carrinho de compras do cliente.
    Responsável por manter o histórico de adições e as quantidades consolidadas por produto (SRP).
    """

    def __init__(self) -> None:
        """Inicializa o carrinho vazio."""
        self._items: list[ProductQuantity] = []
        self._product_quantities: dict[Product, float] = {}

    @property
    def items(self) -> list[ProductQuantity]:
        """Lista com cada registro de adição de item ao carrinho (cópia defensiva)."""
        return self._items[:]

    def add_item(self, product: Product) -> None:
        """Adiciona 1 unidade do produto ao carrinho."""
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self) -> dict[Product, float]:
        """Dicionário consolidado com {produto: quantidade_total} (cópia defensiva)."""
        return self._product_quantities.copy()

    def add_item_quantity(self, product: Product, quantity: float) -> None:
        """Adiciona uma quantidade específica do produto ao carrinho."""
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities:
            self._product_quantities[product] += quantity
        else:
            self._product_quantities[product] = quantity

    def handle_offers(
        self,
        receipt: Receipt,
        offers: dict[Product, Union[OfferStrategy, Offer]],
        catalog: CatalogReader,
    ) -> None:
        """
        Delega o cálculo de descontos para a estratégia (OfferStrategy) associada a cada produto,
        adicionando os descontos elegíveis ao recibo (OCP / SRP).
        """
        offer_factory = OfferFactory()
        for product, quantity in self._product_quantities.items():
            if product in offers:
                offer = offers[product]
                strategy = (
                    offer
                    if isinstance(offer, OfferStrategy)
                    else offer_factory.create_offer(offer.offer_type, offer.argument)
                )
                unit_price = catalog.unit_price(product)
                discount = strategy.calculate_discount(product, quantity, unit_price)
                if discount:
                    receipt.add_discount(discount)
