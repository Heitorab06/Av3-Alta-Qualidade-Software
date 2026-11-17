from abc import ABC, abstractmethod


class CatalogReader(ABC):
    """Interface de leitura do catálogo para consulta de preços e produtos no caixa (ISP/LSP)."""

    @abstractmethod
    def unit_price(self, product):
        """Retorna o preço unitário de um produto."""

    @abstractmethod
    def find_product_by_name(self, name):
        """Busca e retorna um produto pelo nome, ou None caso não exista."""


class CatalogWriter(ABC):
    """Interface de escrita do catálogo para cadastro administrativo de produtos (ISP/LSP)."""

    @abstractmethod
    def add_product(self, product, price):
        """Adiciona um produto e seu preço ao catálogo."""


class SupermarketCatalog(CatalogReader, CatalogWriter):
    """
    Contrato completo para implementações de catálogo que suportam leitura e escrita.
    Herda de CatalogReader e CatalogWriter sem lançar exceções genéricas em métodos base (LSP).
    """



