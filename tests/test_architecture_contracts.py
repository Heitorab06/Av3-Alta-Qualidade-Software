"""Testes de contratos arquiteturais (SOLID, DIP, ISP, LSP e retrocompatibilidade)."""

import pytest

from catalog import CatalogReader, CatalogWriter, SupermarketCatalog
from model_objects import Discount, Product, ProductUnit, SpecialOfferType
from offers import OfferFactory, OfferStrategy
from receipt import Receipt, ReceiptFactory
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog
from tests.receipt_printer import ReceiptPrinter


class ReadOnlyCatalog(CatalogReader):
    """Implementação somente leitura de CatalogReader para validar ISP e LSP."""

    def __init__(self, items: dict[Product, float]) -> None:
        """Inicializa o catálogo somente leitura com mapa de produtos e preços."""
        self._prices = items
        self._by_name = {product.name: product for product in items}

    def unit_price(self, product: Product) -> float:
        """Retorna o preço unitário do produto."""
        return self._prices[product]

    def find_product_by_name(self, name: str) -> Product | None:
        """Busca produto pelo nome."""
        return self._by_name.get(name)


class SpyReceiptFactory(ReceiptFactory):
    """Fábrica espiã para validar injeção de dependência (DIP) no Teller."""

    def __init__(self) -> None:
        """Inicializa contador de recibos criados."""
        self.created_count = 0

    def create_receipt(self) -> Receipt:
        """Cria um Receipt e incrementa o contador de chamadas."""
        self.created_count += 1
        return Receipt()


class FixedFlatDiscountStrategy(OfferStrategy):
    """Estratégia customizada para validar extensão sem modificação (OCP)."""

    def __init__(self, flat_discount: float) -> None:
        """Inicializa a estratégia com valor fixo de abatimento."""
        self._flat_discount = flat_discount

    def calculate_discount(
        self, product: Product, quantity: float, unit_price: float
    ) -> Discount | None:
        """Aplica desconto fixo limitado ao valor bruto do item."""
        gross = quantity * unit_price
        applied = min(self._flat_discount, gross)
        return Discount(product, "flat promo", -applied)


class SpyOfferFactory(OfferFactory):
    """Fábrica espiã para validar injeção de OfferFactory no Teller."""

    def __init__(self) -> None:
        """Inicializa contador de ofertas criadas."""
        self.created_count = 0

    def create_offer(
        self,
        offer_type: SpecialOfferType | OfferStrategy,
        argument: float | None = None,
    ) -> OfferStrategy:
        """Delega criação para OfferFactory e contabiliza a chamada."""
        self.created_count += 1
        return super().create_offer(offer_type, argument)


def test_catalog_abstract_contracts_cannot_be_instantiated() -> None:
    """Garante que interfaces abstratas de catálogo exigem implementação (LSP/ISP)."""
    with pytest.raises(TypeError):
        CatalogReader()  # type: ignore[abstract]
    with pytest.raises(TypeError):
        CatalogWriter()  # type: ignore[abstract]
    with pytest.raises(TypeError):
        SupermarketCatalog()  # type: ignore[abstract]


def test_teller_works_with_read_only_catalog_reader() -> None:
    """Garante que Teller opera apenas com CatalogReader sem add_product (ISP)."""
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    read_only_catalog = ReadOnlyCatalog({toothbrush: 1.25})

    teller = Teller(read_only_catalog)
    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 2)

    receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == pytest.approx(2.50, abs=1e-6)
    assert teller.product_with_name("toothbrush") is toothbrush
    assert not hasattr(read_only_catalog, "add_product")


def test_teller_uses_injected_receipt_and_offer_factories() -> None:
    """Garante uso das fábricas injetadas no Teller (DIP / R08)."""
    catalog = FakeCatalog()
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 2.00)

    receipt_factory = SpyReceiptFactory()
    offer_factory = SpyOfferFactory()
    teller = Teller(
        catalog,
        receipt_factory=receipt_factory,
        offer_factory=offer_factory,
    )

    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 10.0)
    cart = ShoppingCart()
    cart.add_item_quantity(apples, 1.5)
    receipt = teller.checks_out_articles_from(cart)

    assert offer_factory.created_count == 1
    assert receipt_factory.created_count == 1
    assert receipt.total_price() == pytest.approx(2.70, abs=1e-6)


def test_teller_accepts_custom_offer_strategy_without_modification() -> None:
    """Garante extensão com nova OfferStrategy sem alterar Teller ou Cart (OCP)."""
    catalog = FakeCatalog()
    coffee = Product("coffee", ProductUnit.EACH)
    catalog.add_product(coffee, 10.00)

    teller = Teller(catalog)
    teller.add_special_offer(FixedFlatDiscountStrategy(2.50), coffee)

    cart = ShoppingCart()
    cart.add_item(coffee)
    receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == pytest.approx(7.50, abs=1e-6)
    assert len(receipt.discounts) == 1
    assert receipt.discounts[0].description == "flat promo"
    assert receipt.discounts[0].discount_amount == pytest.approx(-2.50, abs=1e-6)


def test_receipt_printer_supports_custom_column_width() -> None:
    """Garante que ReceiptPrinter respeita largura customizada de colunas (R03)."""
    catalog = FakeCatalog()
    milk = Product("milk", ProductUnit.EACH)
    catalog.add_product(milk, 4.50)

    teller = Teller(catalog)
    cart = ShoppingCart()
    cart.add_item(milk)
    receipt = teller.checks_out_articles_from(cart)

    printed = ReceiptPrinter(columns=30).print_receipt(receipt)
    lines = printed.splitlines()

    assert len(lines[0]) == 30
    assert lines[0].startswith("milk")
    assert lines[0].endswith("4.50")
    assert len(lines[-1]) == 30
    assert lines[-1].startswith("Total: ")
    assert lines[-1].endswith("4.50")
