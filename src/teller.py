from model_objects import Offer
from receipt import Receipt


class Teller:
    """
    Representa o operador de caixa do supermercado.
    Responsável por gerenciar as ofertas vigentes e realizar o checkout dos carrinhos de compra.
    """

    def __init__(self, catalog):
        self.catalog = catalog
        self.offers = {}

    def add_special_offer(self, offer_type, product, argument):
        """Cadastra uma promoção/oferta ativa para um produto específico."""
        self.offers[product] = Offer(offer_type, product, argument)

    def checks_out_articles_from(self, the_cart):
        """
        Processa as compras do carrinho:
        1. Cria o recibo.
        2. Consulta o preço unitário e calcula o valor total de cada item.
        3. Delega o cálculo das ofertas e descontos para o carrinho.
        Retorna o recibo finalizado (Receipt).
        """
        receipt = Receipt()
        product_quantities = the_cart.items
        for pq in product_quantities:
            p = pq.product
            quantity = pq.quantity
            unit_price = self.catalog.unit_price(p)
            price = quantity * unit_price
            receipt.add_product(p, quantity, unit_price, price)

        the_cart.handle_offers(receipt, self.offers, self.catalog)

        return receipt

    def product_with_name(self, name):
        """Busca um produto no catálogo pelo nome."""
        return self.catalog.products.get(name, None)
