"""Testes dos 3 níveis da Estratégia de Reversão (Feature Toggle, Fallback e PDV)."""

import pytest

from model_objects import Discount, Offer, Product, ProductUnit, SpecialOfferType
from offers import (
    AmountForQuantityStrategy,
    OfferStrategy,
    calculate_legacy_discount,
    to_legacy_offer,
)
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


class ExplodingStrategy(OfferStrategy):
    """Estratégia defeituosa que lança exceção em runtime para testar fallback."""

    def calculate_discount(
        self, product: Product, quantity: float, unit_price: float
    ) -> Discount | None:
        """Dispara RuntimeError simulando falha inesperada."""
        raise RuntimeError("Falha simulada no motor de estratégias")


class ExcessiveDiscountStrategy(OfferStrategy):
    """Estratégia defeituosa que retorna desconto maior que o valor bruto (INV-03)."""

    def calculate_discount(
        self, product: Product, quantity: float, unit_price: float
    ) -> Discount | None:
        """Retorna abatimento maior que o valor total do item."""
        return Discount(product, "excessive", -(quantity * unit_price + 10.0))


def test_level1_feature_toggle_disabled_uses_legacy_engine(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Garante paridade financeira com ENABLE_STRATEGY_OFFERS=false (Nível 1)."""
    monkeypatch.setenv("ENABLE_STRATEGY_OFFERS", "false")

    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)
    cherry_tomatoes = Product("cherry tomatoes", ProductUnit.EACH)
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    custom_item = Product("custom", ProductUnit.EACH)

    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(apples, 1.99)
    catalog.add_product(cherry_tomatoes, 0.69)
    catalog.add_product(toothpaste, 1.79)
    catalog.add_product(custom_item, 5.00)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 20.0)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, cherry_tomatoes, 0.99)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothpaste, 7.49)
    teller.add_special_offer(AmountForQuantityStrategy(3, 10.0), custom_item)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 3)
    cart.add_item_quantity(apples, 2.0)
    cart.add_item_quantity(cherry_tomatoes, 2)
    cart.add_item_quantity(toothpaste, 5)
    cart.add_item_quantity(custom_item, 3)

    receipt = teller.checks_out_articles_from(cart)

    # 13.64 (4 ofertas legadas) + 15.00 (custom sem equivalente legado) = 28.64
    assert receipt.total_price() == pytest.approx(28.64, abs=0.01)
    assert len(receipt.discounts) == 4


def test_level1_legacy_engine_returns_none_for_ineligible_quantities() -> None:
    """Garante retorno None no motor legado quando quantidade é insuficiente."""
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    offer = Offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)

    assert to_legacy_offer(toothbrush, offer) is offer
    assert calculate_legacy_discount(toothbrush, 2, 0.99, offer) is None


def test_level1_automatic_fallback_on_strategy_exception(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Garante comutação automática segura quando estratégia lança exceção."""
    catalog = FakeCatalog()
    soap = Product("soap", ProductUnit.EACH)
    catalog.add_product(soap, 3.00)

    teller = Teller(catalog)
    teller.add_special_offer(ExplodingStrategy(), soap)

    cart = ShoppingCart()
    cart.add_item_quantity(soap, 2)

    with caplog.at_level("WARNING"):
        receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == pytest.approx(6.00, abs=1e-6)
    assert receipt.discounts == []
    assert "comutando para motor legado" in caplog.text


def test_level1_automatic_fallback_on_inconsistent_discount(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Garante comutação automática quando estratégia viola teto de desconto."""
    catalog = FakeCatalog()
    milk = Product("milk", ProductUnit.EACH)
    catalog.add_product(milk, 4.00)

    teller = Teller(catalog)
    teller.add_special_offer(ExcessiveDiscountStrategy(), milk)

    cart = ShoppingCart()
    cart.add_item_quantity(milk, 1)

    with caplog.at_level("WARNING"):
        receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == pytest.approx(4.00, abs=1e-6)
    assert receipt.discounts == []
    assert "comutando para motor legado" in caplog.text


def test_level3_pdv_emergency_mode_via_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Garante cobrança pelo preço de tabela com PDV_EMERGENCY_MODE=true (Nível 3)."""
    monkeypatch.setenv("PDV_EMERGENCY_MODE", "true")

    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 3)

    receipt = teller.checks_out_articles_from(cart)

    assert teller.emergency_mode is True
    assert receipt.discounts == []
    assert receipt.total_price() == pytest.approx(2.97, abs=1e-6)


def test_level3_pdv_emergency_mode_manual_toggle() -> None:
    """Garante ativação e desativação manual do modo de emergência no Teller."""
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1.00)

    teller = Teller(catalog, emergency_mode=True)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 3)

    emergency_receipt = teller.checks_out_articles_from(cart)
    assert emergency_receipt.discounts == []
    assert emergency_receipt.total_price() == pytest.approx(3.00, abs=1e-6)

    teller.disable_emergency_mode()
    normal_receipt = teller.checks_out_articles_from(cart)
    assert len(normal_receipt.discounts) == 1
    assert normal_receipt.total_price() == pytest.approx(2.00, abs=1e-6)

    teller.enable_emergency_mode()
    emergency_again = teller.checks_out_articles_from(cart)
    assert emergency_again.discounts == []
    assert emergency_again.total_price() == pytest.approx(3.00, abs=1e-6)
