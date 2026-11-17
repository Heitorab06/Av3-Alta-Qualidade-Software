"""Módulo de implementação simulada (in-memory) do catálogo para testes unitários."""

from typing import Optional

from catalog import SupermarketCatalog
from model_objects import Product


class FakeCatalog(SupermarketCatalog):
    """
    Implementação em memória do catálogo para uso em testes de unidade.
    Evita chamadas a bancos de dados externos.
    """

    def __init__(self) -> None:
        """Inicializa os dicionários internos de produtos e preços em memória."""
        self.products: dict[str, Product] = {}
        self.prices: dict[str, float] = {}

    def add_product(self, product: Product, price: float) -> None:
        """Registra o produto e seu respectivo preço unitário, validando preço não negativo."""
        if price < 0.0:
            raise ValueError("O preço unitário não pode ser negativo (INV-04).")
        self.products[product.name] = product
        self.prices[product.name] = price

    def unit_price(self, product: Product) -> float:
        """Retorna o preço unitário do produto cadastrado."""
        return self.prices[product.name]

    def find_product_by_name(self, name: str) -> Optional[Product]:
        """Busca um produto cadastrado pelo nome."""
        return self.products.get(name, None)


