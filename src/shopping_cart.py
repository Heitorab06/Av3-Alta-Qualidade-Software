import math

from model_objects import ProductQuantity, SpecialOfferType, Discount


class ShoppingCart:
    """
    Carrinho de compras do cliente.
    Mantém o histórico de adições e as quantidades consolidadas por produto.
    Também calcula os descontos de cada produto com base nas promoções vigentes.
    """

    def __init__(self):
        self._items = []
        self._product_quantities = {}

    @property
    def items(self):
        """Lista com cada registro de adição de item ao carrinho."""
        return self._items

    def add_item(self, product):
        """Adiciona 1 unidade do produto ao carrinho."""
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self):
        """Dicionário consolidado com {produto: quantidade_total}."""
        return self._product_quantities

    def add_item_quantity(self, product, quantity):
        """Adiciona uma quantidade específica do produto ao carrinho."""
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities.keys():
            self._product_quantities[product] = self._product_quantities[product] + quantity
        else:
            self._product_quantities[product] = quantity

    def handle_offers(self, receipt, offers, catalog):
        """
        Processa as regras de negócio de cada promoção para os produtos presentes no carrinho:
        - THREE_FOR_TWO: Leve 3 pague 2.
        - TWO_FOR_AMOUNT: 2 itens por um valor fechado (ex: 2 por R$ 5,00).
        - FIVE_FOR_AMOUNT: 5 itens por um valor fechado.
        - TEN_PERCENT_DISCOUNT: Desconto percentual direto sobre o valor total do produto.
        Adiciona os descontos elegíveis diretamente no objeto Receipt.
        """
        for p in self._product_quantities.keys():
            quantity = self._product_quantities[p]
            if p in offers.keys():
                offer = offers[p]
                unit_price = catalog.unit_price(p)
                quantity_as_int = int(quantity)
                discount = None
                x = 1
                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
                    x = 3

                elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
                    x = 2
                    if quantity_as_int >= 2:
                        total = offer.argument * (quantity_as_int / x) + quantity_as_int % 2 * unit_price
                        discount_n = unit_price * quantity - total
                        discount = Discount(p, "2 for " + str(offer.argument), -discount_n)

                if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
                    x = 5

                number_of_x = math.floor(quantity_as_int / x)
                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO and quantity_as_int > 2:
                    discount_amount = quantity * unit_price - (
                                (number_of_x * 2 * unit_price) + quantity_as_int % 3 * unit_price)
                    discount = Discount(p, "3 for 2", -discount_amount)

                if offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
                    discount = Discount(p, str(offer.argument) + "% off",
                                        -quantity * unit_price * offer.argument / 100.0)

                if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT and quantity_as_int >= 5:
                    discount_total = unit_price * quantity - (
                                offer.argument * number_of_x + quantity_as_int % 5 * unit_price)
                    discount = Discount(p, str(x) + " for " + str(offer.argument), -discount_total)

                if discount:
                    receipt.add_discount(discount)
