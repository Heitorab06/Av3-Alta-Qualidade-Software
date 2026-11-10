from model_objects import Product, ProductUnit, SpecialOfferType
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog
from tests.receipt_printer import ReceiptPrinter


def test_print_empty_receipt():
    """
    Cenário: Impressão de recibo de um carrinho vazio.
    Objetivo: Garantir que o cabeçalho esteja vazio e o total exiba 0.00 alinhado às 40 colunas.
    """
    catalog = FakeCatalog()
    teller = Teller(catalog)
    cart = ShoppingCart()

    receipt = teller.checks_out_articles_from(cart)
    printed = ReceiptPrinter().print_receipt(receipt)

    expected = (
        "\n"
        "Total:                              0.00\n"
    )
    assert printed == expected


def test_print_receipt_single_each_item():
    """
    Cenário: 1 unidade de produto vendido por unidade (EACH), sem descontos.
    Objetivo: Garantir que não imprime sublinha de detalhamento quando quantidade == 1.
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


def test_print_receipt_kilo_item_and_multiple_quantities():
    """
    Cenário: Produto vendido por quilo (KILO) com quantidade fracionada (2.5 kg)
    e produto por unidade (EACH) com quantidade > 1.
    Objetivo: Validar a formatação com 3 casas decimais para KILO e sublinhas de quantidade.
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


def test_print_receipt_with_discount():
    """
    Cenário: Compra com oferta 'Leve 3 pague 2' aplicada.
    Objetivo: Garantir que a linha de desconto e o total líquido sejam impressos corretamente.
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
