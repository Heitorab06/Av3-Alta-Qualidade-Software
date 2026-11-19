"""Representação de recibos (Receipt), itens faturados e fábrica de recibos."""

from model_objects import Discount, Product


class ReceiptItem:
    """Representa uma linha de item comprado no recibo."""

    def __init__(
        self, product: Product, quantity: float, price: float, total_price: float
    ) -> None:
        """Inicializa o item do recibo com produto, quantidade e valores."""
        self.product: Product = product
        self.quantity: float = quantity
        self.price: float = price
        self.total_price: float = total_price


class Receipt:
    """Comprovante / cupom fiscal de compras.

    Armazena os itens faturados e os descontos concedidos, calculando o total.
    """

    def __init__(self) -> None:
        """Inicializa um recibo vazio sem itens e sem descontos."""
        self._items: list[ReceiptItem] = []
        self._discounts: list[Discount] = []

    def total_price(self) -> float:
        """Calcula o valor final a pagar: soma dos itens mais os descontos."""
        total = 0.0
        for item in self.items:
            total += item.total_price
        for discount in self.discounts:
            total += discount.discount_amount
        return total

    def add_product(
        self, product: Product, quantity: float, price: float, total_price: float
    ) -> None:
        """Registra um item comprado no recibo."""
        self._items.append(ReceiptItem(product, quantity, price, total_price))

    def add_discount(self, discount: Discount) -> None:
        """Registra um desconto concedido no recibo."""
        self._discounts.append(discount)

    @property
    def items(self) -> list[ReceiptItem]:
        """Retorna uma cópia defensiva da lista de itens comprados."""
        return self._items[:]

    @property
    def discounts(self) -> list[Discount]:
        """Retorna uma cópia defensiva da lista de descontos aplicados."""
        return self._discounts[:]


class ReceiptFactory:
    """Fábrica (Factory Method) para criação de instâncias de Receipt (DIP / SRP).

    Desacopla o operador de caixa (Teller) da instanciação direta de Receipt.
    """

    def create_receipt(self) -> Receipt:
        """Cria e retorna uma nova instância de Receipt."""
        return Receipt()
