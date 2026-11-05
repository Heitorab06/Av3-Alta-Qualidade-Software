
class ReceiptItem:
    """Representa uma linha de item comprado no recibo (produto, quantidade, preço unitário e total bruto)."""
    def __init__(self, product, quantity, price, total_price):
        self.product = product
        self.quantity = quantity
        self.price = price
        self.total_price = total_price


class Receipt:
    """
    Comprovante / cupom fiscal de compras.
    Armazena os itens faturados e os descontos concedidos, calculando o valor final total.
    """
    def __init__(self):
        self._items = []
        self._discounts = []

    def total_price(self):
        """Calcula o valor final a pagar: soma dos itens menos/mais os descontos aplicados."""
        total = 0
        for item in self.items:
            total += item.total_price
        for discount in self.discounts:
            total += discount.discount_amount
        return total

    def add_product(self, product, quantity, price, total_price):
        """Registra um item comprado no recibo."""
        self._items.append(ReceiptItem(product, quantity, price, total_price))

    def add_discount(self, discount):
        """Registra um desconto concedido no recibo."""
        self._discounts.append(discount)

    @property
    def items(self):
        """Retorna uma cópia da lista de itens comprados."""
        return self._items[:]

    @property
    def discounts(self):
        """Retorna uma cópia da lista de descontos aplicados."""
        return self._discounts[:]
