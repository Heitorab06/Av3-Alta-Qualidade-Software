"""Testes unitários para o fluxo de checkout, descontos promocionais e recibos."""

import pytest

from model_objects import Discount, Offer, Product, ProductUnit, SpecialOfferType
from offers import (
    AmountForQuantityStrategy,
    OfferFactory,
    PercentageDiscountStrategy,
    ThreeForTwoStrategy,
)
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


def test_ten_percent_discount() -> None:
    """Garante que oferta em outro produto não se aplica a itens não elegíveis.

    Promoção de 10% está ativa para escovas (toothbrush), mas o cliente compra
    apenas maçãs (apples).
    """
    # 1. Configura produtos e preços no catálogo
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)

    # 2. Configura o operador de caixa e cadastra a oferta para 'toothbrush'
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    # 3. Cliente adiciona 2.5 kg de maçãs no carrinho
    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)

    # 4. Finaliza a compra (checkout) gerando o recibo
    receipt = teller.checks_out_articles_from(cart)

    # 5. Asserções: total esperado = 2.5 * 1.99 = 4.975
    assert 4.975 == pytest.approx(receipt.total_price(), 0.01)
    assert [] == receipt.discounts
    assert 1 == len(receipt.items)
    receipt_item = receipt.items[0]
    assert apples == receipt_item.product
    assert 1.99 == receipt_item.price
    assert 2.5 * 1.99 == pytest.approx(receipt_item.total_price, 0.01)
    assert 2.5 == receipt_item.quantity


def test_empty_cart() -> None:
    """Garante total 0, sem itens e sem descontos para carrinho vazio."""
    catalog = FakeCatalog()
    teller = Teller(catalog)
    cart = ShoppingCart()

    receipt = teller.checks_out_articles_from(cart)

    assert 0 == receipt.total_price()
    assert [] == receipt.items
    assert [] == receipt.discounts


def test_cart_without_discount() -> None:
    """Garante o cálculo do valor bruto sem aplicação de descontos."""
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)

    teller = Teller(catalog)
    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 2)
    cart.add_item_quantity(apples, 1.0)

    receipt = teller.checks_out_articles_from(cart)

    # Total esperado: (2 * 0.99) + (1 * 1.99) = 1.98 + 1.99 = 3.97
    assert 3.97 == pytest.approx(receipt.total_price(), 0.01)
    assert [] == receipt.discounts
    assert 2 == len(receipt.items)


def test_ten_percent_discount_applied() -> None:
    """Garante que o desconto percentual de 10% seja calculado e aplicado."""
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 1)

    receipt = teller.checks_out_articles_from(cart)

    # 0.99 - 10% (0.099) = 0.891
    assert 0.891 == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert -0.099 == pytest.approx(receipt.discounts[0].discount_amount, 0.01)
    assert "10.0% off" == receipt.discounts[0].description


def test_three_for_two_discount_exact_quantity() -> None:
    """Garante que na promoção 'Leve 3 pague 2' com 3 itens paga-se apenas 2."""
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 3)

    receipt = teller.checks_out_articles_from(cart)

    # Leva 3, paga 2 -> 2 * 0.99 = 1.98 (desconto de 0.99)
    assert 1.98 == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert -0.99 == pytest.approx(receipt.discounts[0].discount_amount, 0.01)


def test_three_for_two_discount_with_extra_item() -> None:
    """Garante que em 'Leve 3 pague 2' com 4 itens, o 4º paga valor integral."""
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 4)

    receipt = teller.checks_out_articles_from(cart)

    # 3 itens por 1.98 + 1 item por 0.99 = 2.97
    assert 2.97 == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert -0.99 == pytest.approx(receipt.discounts[0].discount_amount, 0.01)


def test_three_for_two_not_enough_items() -> None:
    """Garante que 'Leve 3 pague 2' não é aplicada com apenas 2 itens."""
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 2)

    receipt = teller.checks_out_articles_from(cart)

    assert 1.98 == pytest.approx(receipt.total_price(), 0.01)
    assert [] == receipt.discounts


def test_same_product_added_separately_combines_for_offer() -> None:
    """Garante que o carrinho consolida adições separadas antes da promoção."""
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)

    cart = ShoppingCart()
    cart.add_item(toothbrush)
    cart.add_item(toothbrush)
    cart.add_item(toothbrush)

    receipt = teller.checks_out_articles_from(cart)

    assert 1.98 == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert -0.99 == pytest.approx(receipt.discounts[0].discount_amount, 0.01)


def test_two_for_amount_discount_exact_quantity() -> None:
    """Garante desconto de R$ 1,00 em '2 por R$ 3,00' levando 2 unidades."""
    catalog = FakeCatalog()
    cherry_tomatoes = Product("cherry tomatoes", ProductUnit.EACH)
    catalog.add_product(cherry_tomatoes, 2.00)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, cherry_tomatoes, 3.00)

    cart = ShoppingCart()
    cart.add_item_quantity(cherry_tomatoes, 2)

    receipt = teller.checks_out_articles_from(cart)

    assert 3.00 == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert -1.00 == pytest.approx(receipt.discounts[0].discount_amount, 0.01)


def test_two_for_amount_discount_with_extra_item() -> None:
    """Garante '2 por R$ 3,00' levando 3 unidades (2 por 3,00 + 1 por 2,00)."""
    catalog = FakeCatalog()
    cherry_tomatoes = Product("cherry tomatoes", ProductUnit.EACH)
    catalog.add_product(cherry_tomatoes, 2.00)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, cherry_tomatoes, 3.00)

    cart = ShoppingCart()
    cart.add_item_quantity(cherry_tomatoes, 3)

    receipt = teller.checks_out_articles_from(cart)

    assert 5.00 == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert -1.00 == pytest.approx(receipt.discounts[0].discount_amount, 0.01)


def test_five_for_amount_discount_exact_quantity() -> None:
    """Garante o desconto correto em '5 por R$ 7,49' levando 5 unidades."""
    catalog = FakeCatalog()
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    catalog.add_product(toothpaste, 1.79)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothpaste, 7.49)

    cart = ShoppingCart()
    cart.add_item_quantity(toothpaste, 5)

    receipt = teller.checks_out_articles_from(cart)

    # Bruto: 5 * 1.79 = 8.95 -> Desconto: 8.95 - 7.49 = 1.46 -> Total: 7.49
    assert 7.49 == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert -1.46 == pytest.approx(receipt.discounts[0].discount_amount, 0.01)


def test_five_for_amount_discount_with_extra_item() -> None:
    """Garante '5 por R$ 7,49' levando 6 unidades (5 por 7,49 + 1 por 1,79)."""
    catalog = FakeCatalog()
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    catalog.add_product(toothpaste, 1.79)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothpaste, 7.49)

    cart = ShoppingCart()
    cart.add_item_quantity(toothpaste, 6)

    receipt = teller.checks_out_articles_from(cart)

    assert 9.28 == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert -1.46 == pytest.approx(receipt.discounts[0].discount_amount, 0.01)


# ==============================================================================
# TESTES DA NOVA FUNCIONALIDADE: PROMOÇÃO DE COMBO (TDD / Aguardando Implementação)
# Exemplo de regra assumida nos testes abaixo:
# Combo = 2 pastas de dente (R$ 2,00 cada) + 1 escova (R$ 1,00 cada) = R$ 5,00 bruto
# Com 10% de desconto no combo = desconto de R$ 0,50 -> Total do combo: R$ 4,50
# ==============================================================================


@pytest.mark.skip(
    reason="Aguardando refatoração SOLID e implementação da oferta de Combo"
)
def test_combo_exact_items() -> None:
    """Aplica exatamente 1 desconto de combo para 2 pastas e 1 escova."""
    catalog = FakeCatalog()
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    catalog.add_product(toothpaste, 2.00)
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1.00)

    teller = Teller(catalog)
    # TODO: Registrar a oferta de combo após implementar (ex: ComboOffer)
    # teller.add_special_offer(ComboOffer({toothpaste: 2, toothbrush: 1}, 10.0))

    cart = ShoppingCart()
    cart.add_item_quantity(toothpaste, 2)
    cart.add_item_quantity(toothbrush, 1)

    receipt = teller.checks_out_articles_from(cart)

    assert 4.50 == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert -0.50 == pytest.approx(receipt.discounts[0].discount_amount, 0.01)


@pytest.mark.skip(
    reason="Aguardando refatoração SOLID e implementação da oferta de Combo"
)
def test_combo_with_extra_items_applies_only_once() -> None:
    """Aplica 1 combo para 3 pastas e 1 escova; a 3ª pasta paga preço normal."""
    catalog = FakeCatalog()
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    catalog.add_product(toothpaste, 2.00)
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1.00)

    teller = Teller(catalog)
    # TODO: Registrar a oferta de combo após implementar
    # teller.add_special_offer(ComboOffer({toothpaste: 2, toothbrush: 1}, 10.0))

    cart = ShoppingCart()
    cart.add_item_quantity(toothpaste, 3)
    cart.add_item_quantity(toothbrush, 1)

    receipt = teller.checks_out_articles_from(cart)

    # Bruto: (3 * 2.00) + 1.00 = 7.00 -> 1 combo dá 0.50 de desconto -> Total: 6.50
    assert 6.50 == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert -0.50 == pytest.approx(receipt.discounts[0].discount_amount, 0.01)


@pytest.mark.skip(
    reason="Aguardando refatoração SOLID e implementação da oferta de Combo"
)
def test_combo_incomplete_does_not_apply() -> None:
    """Garante que nenhum desconto é aplicado quando falta item do combo."""
    catalog = FakeCatalog()
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    catalog.add_product(toothpaste, 2.00)
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1.00)

    teller = Teller(catalog)
    # TODO: Registrar a oferta de combo após implementar
    # teller.add_special_offer(ComboOffer({toothpaste: 2, toothbrush: 1}, 10.0))

    cart = ShoppingCart()
    cart.add_item_quantity(toothpaste, 2)

    receipt = teller.checks_out_articles_from(cart)

    assert 4.00 == pytest.approx(receipt.total_price(), 0.01)
    assert [] == receipt.discounts


@pytest.mark.skip(
    reason="Aguardando refatoração SOLID e implementação da oferta de Combo"
)
def test_multiple_combos() -> None:
    """Reconhece e aplica 2 combos completos para 4 pastas e 2 escovas."""
    catalog = FakeCatalog()
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    catalog.add_product(toothpaste, 2.00)
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1.00)

    teller = Teller(catalog)
    # TODO: Registrar a oferta de combo após implementar
    # teller.add_special_offer(ComboOffer({toothpaste: 2, toothbrush: 1}, 10.0))

    cart = ShoppingCart()
    cart.add_item_quantity(toothpaste, 4)
    cart.add_item_quantity(toothbrush, 2)

    receipt = teller.checks_out_articles_from(cart)

    # Bruto: 10.00 -> 2 combos dão 1.00 de desconto -> Total: 9.00
    assert 9.00 == pytest.approx(receipt.total_price(), 0.01)
    assert -1.00 == pytest.approx(
        sum(d.discount_amount for d in receipt.discounts), 0.01
    )


def test_amount_for_quantity_not_enough_items() -> None:
    """Garante que AmountForQuantityStrategy retorna None sem quantidade mínima."""
    catalog = FakeCatalog()
    cherry_tomatoes = Product("cherry tomatoes", ProductUnit.EACH)
    catalog.add_product(cherry_tomatoes, 2.00)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, cherry_tomatoes, 3.00)

    cart = ShoppingCart()
    cart.add_item_quantity(cherry_tomatoes, 1)

    receipt = teller.checks_out_articles_from(cart)

    assert 2.00 == pytest.approx(receipt.total_price(), 0.01)
    assert [] == receipt.discounts


def test_offer_factory_custom_strategy_and_legacy_offer() -> None:
    """Valida OfferFactory com estratégia direta, erro inválido e Offer legado."""
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1.00)

    custom_strategy = ThreeForTwoStrategy()
    factory = OfferFactory()
    assert factory.create_offer(custom_strategy) is custom_strategy

    with pytest.raises(ValueError):
        factory.create_offer("INVALID_OFFER")  # type: ignore[arg-type]

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 3)
    receipt = Teller(catalog).checks_out_articles_from(ShoppingCart())

    legacy_offers = {
        toothbrush: Offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)
    }
    cart.handle_offers(receipt, legacy_offers, catalog)
    assert 1 == len(receipt.discounts)
    assert -1.00 == pytest.approx(receipt.discounts[0].discount_amount, 0.01)


def test_teller_product_with_name() -> None:
    """Garante retorno do produto cadastrado e None para produto inexistente."""
    catalog = FakeCatalog()
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)

    teller = Teller(catalog)

    assert apples == teller.product_with_name("apples")
    assert teller.product_with_name("nonexistent") is None


def test_invariants_validation_rules() -> None:
    """Valida invariantes de negócio INV-02, INV-03, INV-04 e INV-05.

    Garante que valores inválidos de desconto, preço, quantidade e unidade sejam
    rejeitados.
    """
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(toothbrush, 2.00)
    catalog.add_product(apples, 4.00)

    # INV-02: Desconto não pode ser positivo
    with pytest.raises(ValueError):
        Discount(toothbrush, "invalid positive discount", 1.00)

    # INV-03: Percentual fora do intervalo [0, 100]
    with pytest.raises(ValueError):
        PercentageDiscountStrategy(150.0)

    # INV-04: Pacote com quantidade <= 0 ou valor negativo
    with pytest.raises(ValueError):
        AmountForQuantityStrategy(0, 5.0)
    with pytest.raises(ValueError):
        AmountForQuantityStrategy(2, -1.0)

    # INV-04: Preço negativo no catálogo e quantidade <= 0 no carrinho
    with pytest.raises(ValueError):
        catalog.add_product(toothbrush, -0.50)

    cart = ShoppingCart()
    with pytest.raises(ValueError):
        cart.add_item_quantity(toothbrush, 0)
    with pytest.raises(ValueError):
        cart.add_item_quantity(toothbrush, -2)

    # INV-05: Produto EACH exige quantidade inteira
    with pytest.raises(ValueError):
        cart.add_item_quantity(toothbrush, 1.5)


def test_invariant_immutability_and_defensive_copies() -> None:
    """Valida INV-01 e INV-06 (cópias defensivas e imutabilidade pós-checkout)."""
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1.50)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    cart = ShoppingCart()
    cart.add_item(toothbrush)

    # Tentativa de mutar as cópias retornadas pelas propriedades do carrinho
    cart.items.clear()
    cart.product_quantities.clear()
    assert 1 == len(cart.items)
    assert 1.0 == cart.product_quantities[toothbrush]

    receipt = teller.checks_out_articles_from(cart)
    initial_total = receipt.total_price()

    # INV-01: Equação do balanço
    expected_balance = sum(i.total_price for i in receipt.items) + sum(
        d.discount_amount for d in receipt.discounts
    )
    assert expected_balance == pytest.approx(initial_total, 0.001)

    # INV-06: Alterações no carrinho ou listas retornadas não afetam o recibo
    cart.add_item(toothbrush)
    receipt.items.clear()
    receipt.discounts.clear()

    assert 1 == len(receipt.items)
    assert 1 == len(receipt.discounts)
    assert initial_total == pytest.approx(receipt.total_price(), 0.001)
