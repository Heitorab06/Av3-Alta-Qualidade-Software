"""Matriz de testes parametrizados de regressão e testes unitários de estratégias."""

import pytest

from model_objects import Product, ProductUnit, SpecialOfferType
from offers import (
    AmountForQuantityStrategy,
    PercentageDiscountStrategy,
    ThreeForTwoStrategy,
)
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


@pytest.mark.parametrize(
    ("quantity", "expected_discount", "expected_total"),
    [
        (1, None, 0.99),
        (2, None, 1.98),
        (3, -0.99, 1.98),
        (4, -0.99, 2.97),
        (5, -0.99, 3.96),
        (6, -1.98, 3.96),
        (7, -1.98, 4.95),
        (9, -2.97, 5.94),
        (10, -2.97, 6.93),
    ],
)
def test_three_for_two_regression_matrix(
    quantity: int,
    expected_discount: float | None,
    expected_total: float,
) -> None:
    """Valida múltiplos, sobras e quantidades insuficientes em THREE_FOR_TWO."""
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, quantity)
    receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == pytest.approx(expected_total, abs=1e-6)
    if expected_discount is None:
        assert receipt.discounts == []
    else:
        assert len(receipt.discounts) == 1
        discount = receipt.discounts[0]
        assert discount.description == "3 for 2"
        assert discount.discount_amount <= 0.0
        assert discount.discount_amount == pytest.approx(expected_discount, abs=1e-6)
        assert abs(discount.discount_amount) <= quantity * 0.99 + 1e-9


@pytest.mark.parametrize(
    ("quantity", "expected_discount", "expected_total"),
    [
        (1, None, 0.69),
        (2, -0.39, 0.99),
        (3, -0.39, 1.68),
        (4, -0.78, 1.98),
        (5, -0.78, 2.67),
        (6, -1.17, 2.97),
    ],
)
def test_two_for_amount_regression_matrix(
    quantity: int,
    expected_discount: float | None,
    expected_total: float,
) -> None:
    """Valida múltiplos inteiros, sobras e quantidade insuficiente em TWO_FOR_AMOUNT."""
    catalog = FakeCatalog()
    cherry_tomatoes = Product("cherry tomatoes", ProductUnit.EACH)
    catalog.add_product(cherry_tomatoes, 0.69)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, cherry_tomatoes, 0.99)

    cart = ShoppingCart()
    cart.add_item_quantity(cherry_tomatoes, quantity)
    receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == pytest.approx(expected_total, abs=1e-6)
    if expected_discount is None:
        assert receipt.discounts == []
    else:
        assert len(receipt.discounts) == 1
        discount = receipt.discounts[0]
        assert discount.description == "2 for 0.99"
        assert discount.discount_amount <= 0.0
        assert discount.discount_amount == pytest.approx(expected_discount, abs=1e-6)


@pytest.mark.parametrize(
    ("quantity", "expected_discount", "expected_total"),
    [
        (1, None, 1.79),
        (2, None, 3.58),
        (4, None, 7.16),
        (5, -1.46, 7.49),
        (6, -1.46, 9.28),
        (9, -1.46, 14.65),
        (10, -2.92, 14.98),
        (11, -2.92, 16.77),
        (15, -4.38, 22.47),
    ],
)
def test_five_for_amount_regression_matrix(
    quantity: int,
    expected_discount: float | None,
    expected_total: float,
) -> None:
    """Valida múltiplos, sobras e quantidades insuficientes em FIVE_FOR_AMOUNT."""
    catalog = FakeCatalog()
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    catalog.add_product(toothpaste, 1.79)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothpaste, 7.49)

    cart = ShoppingCart()
    cart.add_item_quantity(toothpaste, quantity)
    receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == pytest.approx(expected_total, abs=1e-6)
    if expected_discount is None:
        assert receipt.discounts == []
    else:
        assert len(receipt.discounts) == 1
        discount = receipt.discounts[0]
        assert discount.description == "5 for 7.49"
        assert discount.discount_amount <= 0.0
        assert discount.discount_amount == pytest.approx(expected_discount, abs=1e-6)


@pytest.mark.parametrize(
    ("unit", "unit_price", "quantity", "percent", "expected_discount"),
    [
        (ProductUnit.EACH, 1.00, 1, 0.0, 0.0),
        (ProductUnit.EACH, 1.00, 3, 10.0, -0.30),
        (ProductUnit.EACH, 2.50, 2, 100.0, -5.00),
        (ProductUnit.KILO, 1.99, 0.25, 10.0, -0.04975),
        (ProductUnit.KILO, 1.99, 2.5, 20.0, -0.995),
        (ProductUnit.KILO, 4.00, 1.333, 15.0, -0.7998),
    ],
)
def test_percentage_discount_regression_matrix(
    unit: ProductUnit,
    unit_price: float,
    quantity: float,
    percent: float,
    expected_discount: float,
) -> None:
    """Valida descontos percentuais para produtos EACH e KILO fracionários."""
    catalog = FakeCatalog()
    product = Product("item", unit)
    catalog.add_product(product, unit_price)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, product, percent)

    cart = ShoppingCart()
    cart.add_item_quantity(product, quantity)
    receipt = teller.checks_out_articles_from(cart)

    gross_total = quantity * unit_price
    expected_total = gross_total + expected_discount
    assert len(receipt.discounts) == 1
    assert receipt.discounts[0].description == f"{percent}% off"
    assert receipt.discounts[0].discount_amount == pytest.approx(
        expected_discount, abs=1e-6
    )
    assert receipt.total_price() == pytest.approx(expected_total, abs=1e-6)


@pytest.mark.parametrize(
    ("quantity", "unit_price", "expected_amount"),
    [
        (2.0, 1.50, None),
        (3.0, 1.50, -1.50),
        (8.0, 1.50, -3.00),
    ],
)
def test_three_for_two_strategy_unit(
    quantity: float,
    unit_price: float,
    expected_amount: float | None,
) -> None:
    """Testa isoladamente ThreeForTwoStrategy sem acoplamento com Teller ou Cart."""
    product = Product("soap", ProductUnit.EACH)
    strategy = ThreeForTwoStrategy()

    discount = strategy.calculate_discount(product, quantity, unit_price)

    if expected_amount is None:
        assert discount is None
    else:
        assert discount is not None
        assert discount.product is product
        assert discount.description == "3 for 2"
        assert discount.discount_amount == pytest.approx(expected_amount, abs=1e-6)


@pytest.mark.parametrize(
    ("required_qty", "pack_amount", "quantity", "unit_price", "expected_amount"),
    [
        (2, 3.00, 1.0, 2.00, None),
        (2, 3.00, 2.0, 2.00, -1.00),
        (3, 5.00, 7.0, 2.00, -2.00),
        (5, 0.00, 5.0, 1.50, -7.50),
    ],
)
def test_amount_for_quantity_strategy_unit(
    required_qty: int,
    pack_amount: float,
    quantity: float,
    unit_price: float,
    expected_amount: float | None,
) -> None:
    """Testa isoladamente AmountForQuantityStrategy com vários tamanhos de pacote."""
    product = Product("juice", ProductUnit.EACH)
    strategy = AmountForQuantityStrategy(required_qty, pack_amount)

    discount = strategy.calculate_discount(product, quantity, unit_price)

    if expected_amount is None:
        assert discount is None
    else:
        assert discount is not None
        assert discount.product is product
        assert discount.description == f"{required_qty} for {pack_amount}"
        assert discount.discount_amount == pytest.approx(expected_amount, abs=1e-6)


@pytest.mark.parametrize(
    ("percent", "quantity", "unit_price", "expected_amount"),
    [
        (0.0, 2.0, 5.00, 0.0),
        (12.5, 4.0, 2.00, -1.00),
        (100.0, 1.5, 3.00, -4.50),
    ],
)
def test_percentage_discount_strategy_unit(
    percent: float,
    quantity: float,
    unit_price: float,
    expected_amount: float,
) -> None:
    """Testa isoladamente PercentageDiscountStrategy."""
    product = Product("cheese", ProductUnit.KILO)
    strategy = PercentageDiscountStrategy(percent)

    discount = strategy.calculate_discount(product, quantity, unit_price)

    assert discount is not None
    assert discount.product is product
    assert discount.description == f"{percent}% off"
    assert discount.discount_amount == pytest.approx(expected_amount, abs=1e-6)
