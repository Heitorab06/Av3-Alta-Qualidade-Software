
class SupermarketCatalog:
    """
    Interface/contrato para o catálogo de preços do supermercado.
    Em produção conecta ao banco de dados; em testes usamos uma implementação simulada (FakeCatalog).
    """

    def add_product(self, product, price):
        raise Exception("cannot be called from a unit test - it accesses the database")

    def unit_price(self, product):
        raise Exception("cannot be called from a unit test - it accesses the database")


