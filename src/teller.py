"""Operador de caixa (Teller) responsável por checkout e registro de ofertas."""

from catalog import CatalogReader
from model_objects import Product, SpecialOfferType
from offers import OfferFactory, OfferStrategy
from receipt import Receipt, ReceiptFactory
from shopping_cart import ShoppingCart


class Teller:
    """Representa o operador de caixa do supermercado.

    Gerencia as ofertas vigentes e realiza o checkout dos carrinhos de compra.
    """

    def __init__(
        self,
        catalog: CatalogReader,
        receipt_factory: ReceiptFactory | None = None,
        offer_factory: OfferFactory | None = None,
    ) -> None:
        """Inicializa o caixa com catálogo de leitura e fábricas opcionais."""
        self.catalog: CatalogReader = catalog
        self.receipt_factory: ReceiptFactory = receipt_factory or ReceiptFactory()
        self.offer_factory: OfferFactory = offer_factory or OfferFactory()
        self.offers: dict[Product, OfferStrategy] = {}

    def add_special_offer(
        self,
        offer_type: SpecialOfferType | OfferStrategy,
        product: Product,
        argument: float | None = None,
    ) -> None:
        """Cadastra uma oferta ativa para um produto usando a fábrica de ofertas."""
        self.offers[product] = self.offer_factory.create_offer(offer_type, argument)

    def checks_out_articles_from(self, the_cart: ShoppingCart) -> Receipt:
        """Processa as compras do carrinho e retorna o recibo finalizado.

        1. Cria o recibo por meio da fábrica (ReceiptFactory).
        2. Consulta o preço unitário e calcula o valor total de cada item.
        3. Delega o cálculo das ofertas e descontos.
        """
        receipt = self.receipt_factory.create_receipt()
        product_quantities = the_cart.items
        for product_quantity in product_quantities:
            product = product_quantity.product
            quantity = product_quantity.quantity
            unit_price = self.catalog.unit_price(product)
            price = quantity * unit_price
            receipt.add_product(product, quantity, unit_price, price)

        the_cart.handle_offers(receipt, self.offers, self.catalog)

        return receipt

    def product_with_name(self, name: str) -> Product | None:
        """Busca um produto no catálogo pelo nome via contrato CatalogReader."""
        return self.catalog.find_product_by_name(name)
