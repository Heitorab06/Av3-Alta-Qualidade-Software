from enum import Enum


class ProductUnit(Enum):
    """Define a unidade de medida do produto: por unidade (EACH) ou por quilo (KILO)."""
    EACH = 1
    KILO = 2


class SpecialOfferType(Enum):
    """Tipos de ofertas e promoções disponíveis no supermercado."""
    THREE_FOR_TWO = 1       # Leve 3 pague 2
    TEN_PERCENT_DISCOUNT = 2 # Desconto percentual direto
    TWO_FOR_AMOUNT = 3       # 2 itens por um valor fixo
    FIVE_FOR_AMOUNT = 4      # 5 itens por um valor fixo


class Product:
    """Representa um produto comercializado no supermercado."""
    def __init__(self, name, unit):
        self.name = name
        self.unit = unit


class ProductQuantity:
    """Associa um produto à quantidade inserida no carrinho."""
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity


class Offer:
    """Configuração de uma oferta para um produto específico (tipo da oferta e seu argumento/valor)."""
    def __init__(self, offer_type, product, argument):
        self.offer_type = offer_type
        self.product = product
        self.argument = argument


class Discount:
    """Representa o desconto calculado a ser aplicado no recibo de um produto."""
    def __init__(self, product, description, discount_amount):
        self.product = product
        self.description = description
        self.discount_amount = discount_amount

