"""Testes unitários para formatação e impressão de cupons via ReceiptPrinter."""

from model_objects import Product, ProductUnit, SpecialOfferType
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog
from tests.receipt_printer import ReceiptPrinter


def test_print_empty_receipt() -> None:
    """Valida a impressão de recibo para carrinho vazio.

    Garante que o cabeçalho esteja vazio e o total exiba 0.00 em 40 colunas.
    """
    catalog = FakeCatalog()
    teller = Teller(catalog)
    cart = ShoppingCart()

    receipt = teller.checks_out_articles_from(cart)
    printed = ReceiptPrinter().print_receipt(receipt)

    expected = "\nTotal:                              0.00\n"
    assert printed == expected


def test_print_receipt_single_each_item() -> None:
    """Valida a impressão de 1 unidade de produto EACH sem descontos.

    Garante que não imprime sublinha de detalhamento quando quantidade == 1.
    """
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    teller = Teller(catalog)
    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 1)

    receipt = teller.checks_out_articles_from(cart)
    printed = ReceiptPrinter().print_receipt(receipt)

    expected = (
        "toothbrush                          0.99\n"
        "\n"
        "Total:                              0.99\n"
    )
    assert printed == expected


def test_print_receipt_kilo_item_and_multiple_quantities() -> None:
    """Valida impressão de item KILO fracionado e item EACH com quantidade > 1.

    Valida 3 casas decimais para KILO e sublinhas de quantidade.
    """
    catalog = FakeCatalog()
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 2.00)
    soap = Product("soap", ProductUnit.EACH)
    catalog.add_product(soap, 1.50)

    teller = Teller(catalog)
    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)
    cart.add_item_quantity(soap, 2)

    receipt = teller.checks_out_articles_from(cart)
    printed = ReceiptPrinter().print_receipt(receipt)

    expected = (
        "apples                              5.00\n"
        "  2.00 * 2.500\n"
        "soap                                3.00\n"
        "  1.50 * 2\n"
        "\n"
        "Total:                              8.00\n"
    )
    assert printed == expected


def test_print_receipt_with_discount() -> None:
    """Valida impressão de cupom com oferta 'Leve 3 pague 2' aplicada.

    Garante que a linha de desconto e o total líquido sejam impressos.
    """
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 3)

    receipt = teller.checks_out_articles_from(cart)
    printed = ReceiptPrinter().print_receipt(receipt)

    expected = (
        "toothbrush                          2.97\n"
        "  0.99 * 3\n"
        "3 for 2 (toothbrush)               -0.99\n"
        "\n"
        "Total:                              1.98\n"
    )
    assert printed == expected


def test_print_receipt_mixed_offers_and_items() -> None:
    """Valida impressão de compra mista com múltiplos produtos e ofertas ativas.

    Cobre a formatação completa do cupom em cenários combinados.
    """
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    catalog.add_product(toothpaste, 1.79)
    cherry_tomatoes = Product("cherry tomatoes", ProductUnit.EACH)
    catalog.add_product(cherry_tomatoes, 0.69)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 20.0)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothpaste, 7.49)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, cherry_tomatoes, 0.99)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 3)
    cart.add_item_quantity(apples, 2.0)
    cart.add_item_quantity(toothpaste, 5)
    cart.add_item_quantity(cherry_tomatoes, 2)

    receipt = teller.checks_out_articles_from(cart)
    printed = ReceiptPrinter().print_receipt(receipt)

    expected = (
        "toothbrush                          2.97\n"
        "  0.99 * 3\n"
        "apples                              3.98\n"
        "  1.99 * 2.000\n"
        "toothpaste                          8.95\n"
        "  1.79 * 5\n"
        "cherry tomatoes                     1.38\n"
        "  0.69 * 2\n"
        "3 for 2 (toothbrush)               -0.99\n"
        "20.0% off (apples)                 -0.80\n"
        "5 for 7.49 (toothpaste)            -1.46\n"
        "2 for 0.99 (cherry tomatoes)       -0.39\n"
        "\n"
        "Total:                             13.64\n"
    )
    assert printed == expected
