"""Testes de caracterização (Golden Master / ApprovalTests) para cupons fiscais."""

from approvaltests import verify

from model_objects import Product, ProductUnit, SpecialOfferType
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog
from tests.receipt_printer import ReceiptPrinter


def test_approval_empty_cart() -> None:
    """Valida o cupom Golden Master para carrinho vazio."""
    catalog = FakeCatalog()
    teller = Teller(catalog)
    cart = ShoppingCart()

    receipt = teller.checks_out_articles_from(cart)
    verify(ReceiptPrinter().print_receipt(receipt))


def test_approval_each_and_kilo_without_discount() -> None:
    """Valida o cupom Golden Master para itens EACH e KILO sem desconto."""
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)
    rice = Product("rice", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(apples, 1.99)
    catalog.add_product(rice, 2.49)

    teller = Teller(catalog)
    cart = ShoppingCart()
    cart.add_item(toothbrush)
    cart.add_item_quantity(apples, 2.5)
    cart.add_item_quantity(rice, 2)

    receipt = teller.checks_out_articles_from(cart)
    verify(ReceiptPrinter().print_receipt(receipt))


def test_approval_three_for_two_isolated() -> None:
    """Valida o cupom Golden Master para a oferta THREE_FOR_TWO isolada."""
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 3)

    receipt = teller.checks_out_articles_from(cart)
    verify(ReceiptPrinter().print_receipt(receipt))


def test_approval_ten_percent_discount_isolated() -> None:
    """Valida o cupom Golden Master para a oferta TEN_PERCENT_DISCOUNT isolada."""
    catalog = FakeCatalog()
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 10.0)

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)

    receipt = teller.checks_out_articles_from(cart)
    verify(ReceiptPrinter().print_receipt(receipt))


def test_approval_two_for_amount_isolated() -> None:
    """Valida o cupom Golden Master para a oferta TWO_FOR_AMOUNT isolada."""
    catalog = FakeCatalog()
    cherry_tomatoes = Product("cherry tomatoes", ProductUnit.EACH)
    catalog.add_product(cherry_tomatoes, 0.69)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, cherry_tomatoes, 0.99)

    cart = ShoppingCart()
    cart.add_item_quantity(cherry_tomatoes, 2)

    receipt = teller.checks_out_articles_from(cart)
    verify(ReceiptPrinter().print_receipt(receipt))


def test_approval_five_for_amount_isolated() -> None:
    """Valida o cupom Golden Master para a oferta FIVE_FOR_AMOUNT isolada."""
    catalog = FakeCatalog()
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    catalog.add_product(toothpaste, 1.79)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothpaste, 7.49)

    cart = ShoppingCart()
    cart.add_item_quantity(toothpaste, 5)

    receipt = teller.checks_out_articles_from(cart)
    verify(ReceiptPrinter().print_receipt(receipt))


def test_approval_mixed_products_with_and_without_offers() -> None:
    """Valida o cupom Golden Master com combinação mista de itens com e sem oferta."""
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    cherry_tomatoes = Product("cherry tomatoes", ProductUnit.EACH)
    bread = Product("bread", ProductUnit.EACH)
    bananas = Product("bananas", ProductUnit.KILO)

    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(apples, 1.99)
    catalog.add_product(toothpaste, 1.79)
    catalog.add_product(cherry_tomatoes, 0.69)
    catalog.add_product(bread, 3.50)
    catalog.add_product(bananas, 2.20)

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
    cart.add_item(bread)
    cart.add_item_quantity(bananas, 1.25)

    receipt = teller.checks_out_articles_from(cart)
    verify(ReceiptPrinter().print_receipt(receipt))


def test_approval_ineligible_quantities() -> None:
    """Valida o cupom Golden Master para quantidades abaixo do mínimo da oferta."""
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    cherry_tomatoes = Product("cherry tomatoes", ProductUnit.EACH)
    toothpaste = Product("toothpaste", ProductUnit.EACH)

    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(cherry_tomatoes, 0.69)
    catalog.add_product(toothpaste, 1.79)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, cherry_tomatoes, 0.99)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothpaste, 7.49)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 2)
    cart.add_item_quantity(cherry_tomatoes, 1)
    cart.add_item_quantity(toothpaste, 4)

    receipt = teller.checks_out_articles_from(cart)
    verify(ReceiptPrinter().print_receipt(receipt))


def test_approval_excess_volumes() -> None:
    """Valida o cupom Golden Master com múltiplos pacotes e sobras excedentes."""
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    cherry_tomatoes = Product("cherry tomatoes", ProductUnit.EACH)
    toothpaste = Product("toothpaste", ProductUnit.EACH)

    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(cherry_tomatoes, 0.69)
    catalog.add_product(toothpaste, 1.79)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, cherry_tomatoes, 0.99)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothpaste, 7.49)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 7)
    cart.add_item_quantity(cherry_tomatoes, 5)
    cart.add_item_quantity(toothpaste, 12)

    receipt = teller.checks_out_articles_from(cart)
    verify(ReceiptPrinter().print_receipt(receipt))
