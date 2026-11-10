import pytest

from model_objects import Product, SpecialOfferType, ProductUnit
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


def test_ten_percent_discount():
    """
    Cenário: Uma promoção de 10% está ativa para escovas de dente (toothbrush),
    mas o cliente compra apenas maçãs (apples).
    Objetivo: Garantir que nenhuma promoção seja aplicada indevidamente a itens não elegíveis.
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

    # 5. Asserções:
    # O total a pagar deve ser exatamente 2.5 * 1.99 = 4.975
    assert 4.975 == pytest.approx(receipt.total_price(), 0.01)
    # Nenhum desconto deve ser aplicado
    assert [] == receipt.discounts
    # Deve conter apenas 1 linha/item no recibo
    assert 1 == len(receipt.items)
    receipt_item = receipt.items[0]
    assert apples == receipt_item.product
    assert 1.99 == receipt_item.price
    assert 2.5 * 1.99 == pytest.approx(receipt_item.total_price, 0.01)
    assert 2.5 == receipt_item.quantity


def test_empty_cart():
    """
    Cenário: Cliente finaliza a compra com o carrinho vazio.
    Objetivo: Garantir que o total seja 0 e não existam itens nem descontos no recibo.
    """
    catalog = FakeCatalog()
    teller = Teller(catalog)
    cart = ShoppingCart()

    receipt = teller.checks_out_articles_from(cart)

    assert 0 == receipt.total_price()
    assert [] == receipt.items
    assert [] == receipt.discounts


def test_cart_without_discount():
    """
    Cenário: Carrinho com múltiplos produtos sem nenhuma promoção ativa no caixa.
    Objetivo: Garantir o cálculo do valor bruto sem aplicação de descontos.
    """
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


def test_ten_percent_discount_applied():
    """
    Cenário: Escova de dente tem 10% de desconto e o cliente compra 1 escova.
    Objetivo: Garantir que o desconto percentual de 10% seja calculado e aplicado no recibo.
    """
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


def test_three_for_two_discount_exact_quantity():
    """
    Cenário: Promoção 'Leve 3 pague 2' com exatamente 3 itens no carrinho.
    Objetivo: Garantir que o cliente pague apenas por 2 unidades.
    """
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


def test_three_for_two_discount_with_extra_item():
    """
    Cenário: Promoção 'Leve 3 pague 2' com 4 itens no carrinho.
    Objetivo: 3 itens entram na promoção (paga 2) e o 4º item paga o valor integral.
    """
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


def test_three_for_two_not_enough_items():
    """
    Cenário: Promoção 'Leve 3 pague 2' com apenas 2 itens no carrinho.
    Objetivo: Garantir que a promoção não seja aplicada antes de atingir a quantidade mínima.
    """
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


def test_same_product_added_separately_combines_for_offer():
    """
    Cenário: Mesmo produto adicionado 1 unidade por vez (3 chamadas de add_item).
    Objetivo: Garantir que o carrinho consolida as quantidades antes de aplicar a promoção.
    """
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


def test_two_for_amount_discount_exact_quantity():
    """
    Cenário: Promoção '2 por R$ 3,00' em um item que custa R$ 2,00 cada.
    Objetivo: Garantir o desconto de R$ 1,00 ao levar exatamente 2 unidades.
    """
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


@pytest.mark.xfail(
    reason="Bug existente no código legado: shopping_cart.py linha 62 usa divisão '/' em vez de '//'",
    strict=True,
)
def test_two_for_amount_discount_with_extra_item():
    """
    Cenário: Promoção '2 por R$ 3,00' levando 3 unidades (R$ 2,00 cada).
    Objetivo: 2 itens saem por R$ 3,00 + 1 item avulso por R$ 2,00 = R$ 5,00.
    Nota: Atualmente falha devido a um bug no cálculo de divisão de float no código original.
    """
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


def test_five_for_amount_discount_exact_quantity():
    """
    Cenário: Promoção '5 por R$ 7,49' em pasta de dente que custa R$ 1,79 cada.
    Objetivo: Garantir o desconto correto ao levar exatamente 5 unidades.
    """
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


def test_five_for_amount_discount_with_extra_item():
    """
    Cenário: Promoção '5 por R$ 7,49' levando 6 unidades (R$ 1,79 cada).
    Objetivo: 5 itens saem por R$ 7,49 + 1 item avulso por R$ 1,79 = R$ 9,28.
    """
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


@pytest.mark.skip(reason="Aguardando refatoração SOLID e implementação da oferta de Combo")
def test_combo_exact_items():
    """
    Cenário: Carrinho com exatamente 2 pastas de dente e 1 escova de dente.
    Objetivo: Aplicar exatamente 1 desconto de combo.
    """
    catalog = FakeCatalog()
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    catalog.add_product(toothpaste, 2.00)
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1.00)

    teller = Teller(catalog)
    # TODO: Registrar a oferta de combo após implementar (ex: ComboOffer)
    # teller.add_special_offer(ComboOffer({toothpaste: 2, toothbrush: 1}, discount_percent=10.0))

    cart = ShoppingCart()
    cart.add_item_quantity(toothpaste, 2)
    cart.add_item_quantity(toothbrush, 1)

    receipt = teller.checks_out_articles_from(cart)

    assert 4.50 == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert -0.50 == pytest.approx(receipt.discounts[0].discount_amount, 0.01)


@pytest.mark.skip(reason="Aguardando refatoração SOLID e implementação da oferta de Combo")
def test_combo_with_extra_items_applies_only_once():
    """
    Cenário: Carrinho com 3 pastas de dente e 1 escova de dente.
    Objetivo: Como falta outra escova, forma apenas 1 combo. A 3ª pasta paga preço normal.
    """
    catalog = FakeCatalog()
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    catalog.add_product(toothpaste, 2.00)
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1.00)

    teller = Teller(catalog)
    # TODO: Registrar a oferta de combo após implementar
    # teller.add_special_offer(ComboOffer({toothpaste: 2, toothbrush: 1}, discount_percent=10.0))

    cart = ShoppingCart()
    cart.add_item_quantity(toothpaste, 3)
    cart.add_item_quantity(toothbrush, 1)

    receipt = teller.checks_out_articles_from(cart)

    # Bruto: (3 * 2.00) + 1.00 = 7.00 -> 1 combo dá 0.50 de desconto -> Total: 6.50
    assert 6.50 == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    assert -0.50 == pytest.approx(receipt.discounts[0].discount_amount, 0.01)


@pytest.mark.skip(reason="Aguardando refatoração SOLID e implementação da oferta de Combo")
def test_combo_incomplete_does_not_apply():
    """
    Cenário: Carrinho com 2 pastas de dente, mas nenhuma escova.
    Objetivo: Garantir que nenhum desconto seja aplicado se faltar algum item do combo.
    """
    catalog = FakeCatalog()
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    catalog.add_product(toothpaste, 2.00)
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1.00)

    teller = Teller(catalog)
    # TODO: Registrar a oferta de combo após implementar
    # teller.add_special_offer(ComboOffer({toothpaste: 2, toothbrush: 1}, discount_percent=10.0))

    cart = ShoppingCart()
    cart.add_item_quantity(toothpaste, 2)

    receipt = teller.checks_out_articles_from(cart)

    assert 4.00 == pytest.approx(receipt.total_price(), 0.01)
    assert [] == receipt.discounts


@pytest.mark.skip(reason="Aguardando refatoração SOLID e implementação da oferta de Combo")
def test_multiple_combos():
    """
    Cenário: Carrinho com 4 pastas de dente e 2 escovas de dente.
    Objetivo: Deve reconhecer e aplicar 2 combos completos.
    """
    catalog = FakeCatalog()
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    catalog.add_product(toothpaste, 2.00)
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 1.00)

    teller = Teller(catalog)
    # TODO: Registrar a oferta de combo após implementar
    # teller.add_special_offer(ComboOffer({toothpaste: 2, toothbrush: 1}, discount_percent=10.0))

    cart = ShoppingCart()
    cart.add_item_quantity(toothpaste, 4)
    cart.add_item_quantity(toothbrush, 2)

    receipt = teller.checks_out_articles_from(cart)

    # Bruto: 10.00 -> 2 combos dão 1.00 de desconto -> Total: 9.00
    assert 9.00 == pytest.approx(receipt.total_price(), 0.01)
    assert -1.00 == pytest.approx(sum(d.discount_amount for d in receipt.discounts), 0.01)


