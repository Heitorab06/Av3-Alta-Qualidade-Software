"""Entidades e objetos de domínio (produtos, unidades, ofertas e descontos)."""

from enum import Enum


class ProductUnit(Enum):
    """Define a unidade de medida do produto: unidade (EACH) ou quilo (KILO)."""

    EACH = 1
    KILO = 2


class SpecialOfferType(Enum):
    """Tipos de ofertas e promoções disponíveis no supermercado."""

    THREE_FOR_TWO = 1  # Leve 3 pague 2
    TEN_PERCENT_DISCOUNT = 2  # Desconto percentual direto
    TWO_FOR_AMOUNT = 3  # 2 itens por um valor fixo
    FIVE_FOR_AMOUNT = 4  # 5 itens por um valor fixo


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
    """Configuração de oferta para um produto (tipo da oferta e argumento/valor)."""

    def __init__(
        self,
        offer_type: SpecialOfferType,
        product: Product,
        argument: float | None = None,
    ) -> None:
        """Inicializa a oferta associando tipo promocional, produto e argumento."""
        self.offer_type: SpecialOfferType = offer_type
        self.product: Product = product
        self.argument: float | None = argument


class Discount:
    """Representa o desconto calculado a ser aplicado no recibo de um produto."""

    def __init__(
        self, product: Product, description: str, discount_amount: float
    ) -> None:
        """Inicializa o desconto com produto, descrição textual e valor abatido."""
        if discount_amount > 0.0:
            raise ValueError(
                "O valor do desconto deve ser menor ou igual a zero (INV-02)."
            )
        self.product: Product = product
        self.description: str = description
        self.discount_amount: float = discount_amount
