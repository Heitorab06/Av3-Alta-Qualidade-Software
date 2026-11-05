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

