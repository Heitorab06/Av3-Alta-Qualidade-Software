from catalog import SupermarketCatalog


class FakeCatalog(SupermarketCatalog):
    """
    Implementação em memória do catálogo para uso em testes de unidade.
    Evita chamadas a bancos de dados externos.
    """
    def __init__(self):
        self.products = {}
        self.prices = {}

    def add_product(self, product, price):
        """Registra o produto e seu respectivo preço unitário."""
        self.products[product.name] = product
        self.prices[product.name] = price

    def unit_price(self, product):
        """Retorna o preço unitário do produto cadastrado."""
        return self.prices[product.name]

    def find_product_by_name(self, name):
        """Busca um produto cadastrado pelo nome."""
        return self.products.get(name, None)


