"""Módulo do carrinho de compras responsável pelo armazenamento e consolidação de itens."""

from model_objects import ProductQuantity
from offers import OfferFactory, OfferStrategy


class ShoppingCart:
    """
    Carrinho de compras do cliente.
    Responsável por manter o histórico de adições e as quantidades consolidadas por produto (SRP).
    """

    def __init__(self):
        """Inicializa o carrinho vazio."""
        self._items = []
        self._product_quantities = {}

    @property
    def items(self):
        """Lista com cada registro de adição de item ao carrinho (cópia defensiva)."""
        return self._items[:]

    def add_item(self, product):
        """Adiciona 1 unidade do produto ao carrinho."""
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self):
        """Dicionário consolidado com {produto: quantidade_total} (cópia defensiva)."""
        return self._product_quantities.copy()

    def add_item_quantity(self, product, quantity):
        """Adiciona uma quantidade específica do produto ao carrinho."""
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities:
            self._product_quantities[product] += quantity
        else:
            self._product_quantities[product] = quantity

    def handle_offers(self, receipt, offers, catalog):
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
