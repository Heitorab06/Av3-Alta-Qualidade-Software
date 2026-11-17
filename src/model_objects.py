"""Módulo de entidades e objetos de domínio do supermercado (produtos, unidades, ofertas e descontos)."""

from enum import Enum
from typing import Optional


class ProductUnit(Enum):
    """Define a unidade de medida do produto: por unidade (EACH) ou por quilo (KILO)."""

    EACH = 1
    KILO = 2


class SpecialOfferType(Enum):
    """Tipos de ofertas e promoções disponíveis no supermercado."""

    THREE_FOR_TWO = 1        # Leve 3 pague 2
    TEN_PERCENT_DISCOUNT = 2  # Desconto percentual direto
    TWO_FOR_AMOUNT = 3       # 2 itens por um valor fixo
    FIVE_FOR_AMOUNT = 4      # 5 itens por um valor fixo


class Product:
    """Representa um produto comercializado no supermercado."""

    def __init__(self, name: str, unit: ProductUnit) -> None:
        """Inicializa o produto com seu nome e unidade de comercialização."""
        self.name: str = name
        self.unit: ProductUnit = unit


class ProductQuantity:
    """Associa um produto à quantidade inserida no carrinho."""

    def __init__(self, product: Product, quantity: float) -> None:
        """Inicializa o registro contendo o produto e a quantidade correspondente."""
        self.product: Product = product
        self.quantity: float = quantity


class Offer:
    """Configuração de uma oferta para um produto específico (tipo da oferta e seu argumento/valor)."""

    def __init__(
        self,
        offer_type: SpecialOfferType,
        product: Product,
        argument: Optional[float] = None,
    ) -> None:
        """Inicializa a oferta associando o tipo promocional, o produto e o argumento da regra."""
        self.offer_type: SpecialOfferType = offer_type
        self.product: Product = product
        self.argument: Optional[float] = argument


class Discount:
    """Representa o desconto calculado a ser aplicado no recibo de um produto."""

    def __init__(self, product: Product, description: str, discount_amount: float) -> None:
        """Inicializa o desconto com o produto beneficiado, a descrição textual e o valor abatido."""
        if discount_amount > 0.0:
            raise ValueError("O valor do desconto deve ser menor ou igual a zero (INV-02).")
        self.product: Product = product
        self.description: str = description
        self.discount_amount: float = discount_amount

