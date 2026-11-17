"""Módulo do operador de caixa (Teller) responsável pelo fluxo de checkout e registro de ofertas."""

from offers import OfferFactory
from receipt import ReceiptFactory


class Teller:
    """
    Representa o operador de caixa do supermercado.
    Responsável por gerenciar as ofertas vigentes e realizar o checkout dos carrinhos de compra.
    """

    def __init__(self, catalog, receipt_factory=None, offer_factory=None):
        """Inicializa o operador de caixa com o catálogo de leitura e as fábricas de recibo e oferta."""
        self.catalog = catalog
        self.receipt_factory = receipt_factory or ReceiptFactory()
        self.offer_factory = offer_factory or OfferFactory()
        self.offers = {}

    def add_special_offer(self, offer_type, product, argument=None):
        """Cadastra uma promoção/oferta ativa para um produto específico usando a fábrica de ofertas."""
        self.offers[product] = self.offer_factory.create_offer(offer_type, argument)

    def checks_out_articles_from(self, the_cart):
        """
        Processa as compras do carrinho:
        1. Cria o recibo por meio da fábrica (ReceiptFactory).
        2. Consulta o preço unitário e calcula o valor total de cada item.
        3. Delega o cálculo das ofertas e descontos.
        Retorna o recibo finalizado (Receipt).
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

    def product_with_name(self, name):
        """Busca um produto no catálogo pelo nome por meio do contrato de leitura (CatalogReader)."""
        return self.catalog.find_product_by_name(name)
