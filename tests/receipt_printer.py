"""Módulo responsável pela formatação e impressão textual de cupons fiscais (Receipt)."""

from model_objects import ProductUnit


class ReceiptPrinter:
    """Formata um objeto Receipt em texto alinhado por colunas para emissão de cupom."""

    def __init__(self, columns=40):
        """Inicializa a impressora definindo a largura padrão de colunas do cupom."""
        self.columns = columns

    def print_receipt(self, receipt):
        """Gera a representação textual completa do recibo com itens, descontos e valor total."""
        result = ""
        for item in receipt.items:
            receipt_item = self.print_receipt_item(item)
            result += receipt_item

        for discount in receipt.discounts:
            discount_presentation = self.print_discount(discount)
            result += discount_presentation

        result += "\n"
        result += self.present_total(receipt)
        return str(result)

    def print_receipt_item(self, item):
        """Formata a linha principal de um item comprado e a sublinha quando a quantidade difere de 1."""
        total_price_printed = self.print_price(item.total_price)
        name = item.product.name
        line = self.format_line_with_whitespace(name, total_price_printed)
        if item.quantity != 1:
            line += f"  {self.print_price(item.price)} * {self.print_quantity(item)}\n"
        return line

    def format_line_with_whitespace(self, name, value):
        """Alinha o nome à esquerda e o valor à direita preenchendo o espaço intermediário."""
        whitespace_size = self.columns - len(name) - len(value)
        whitespace = " " * whitespace_size
        return f"{name}{whitespace}{value}\n"

    def print_price(self, price):
        """Formata um valor monetário com duas casas decimais."""
        return f"{price:.2f}"

    def print_quantity(self, item):
        """Formata a quantidade do item conforme sua unidade (inteiro para EACH, 3 casas para KILO)."""
        if ProductUnit.EACH == item.product.unit:
            return str(item.quantity)
        return f"{item.quantity:.3f}"

    def print_discount(self, discount):
        """Formata a linha de descrição e valor de um desconto concedido."""
        name = f"{discount.description} ({discount.product.name})"
        value = self.print_price(discount.discount_amount)
        return self.format_line_with_whitespace(name, value)

    def present_total(self, receipt):
        """Formata a linha final com o valor total líquido do recibo."""
        name = "Total: "
        value = self.print_price(receipt.total_price())
        return self.format_line_with_whitespace(name, value)

