"""Operador de caixa (Teller) responsável por checkout e registro de ofertas."""

from catalog import CatalogReader
from model_objects import Product, SpecialOfferType
from offers import ComboOffer, OfferFactory, OfferStrategy, is_pdv_emergency_mode
from receipt import Receipt, ReceiptFactory
from shopping_cart import ShoppingCart


class Teller:
    """Representa o operador de caixa do supermercado.

    Gerencia as ofertas vigentes, o modo de emergência manual (Nível 3)
    e realiza o checkout dos carrinhos de compra.
    """

    def __init__(
        self,
        catalog: CatalogReader,
        receipt_factory: ReceiptFactory | None = None,
        offer_factory: OfferFactory | None = None,
        emergency_mode: bool | None = None,
    ) -> None:
        """Inicializa o caixa com catálogo, fábricas opcionais e modo de emergência."""
        self.catalog: CatalogReader = catalog
        self.receipt_factory: ReceiptFactory = receipt_factory or ReceiptFactory()
        self.offer_factory: OfferFactory = offer_factory or OfferFactory()
        self._emergency_mode: bool | None = emergency_mode
        self.offers: dict[Product, OfferStrategy] = {}
        self.combo_offers: list[ComboOffer] = []

    @property
    def emergency_mode(self) -> bool:
        """Indica se o caixa está em modo de emergência sem promoções (Nível 3)."""
        if self._emergency_mode is not None:
            return self._emergency_mode
        return is_pdv_emergency_mode()

    def enable_emergency_mode(self) -> None:
        """Ativa o modo de emergência manual no PDV (preço direto de tabela)."""
        self._emergency_mode = True

    def disable_emergency_mode(self) -> None:
        """Desativa o modo de emergência manual no PDV, retomando promoções."""
        self._emergency_mode = False

    def add_special_offer(
        self,
        offer_type: SpecialOfferType | OfferStrategy | ComboOffer,
        product: Product | None = None,
        argument: float | None = None,
    ) -> None:
        """Cadastra uma oferta individual de produto ou uma oferta de combo."""
        if isinstance(offer_type, ComboOffer):
            self.combo_offers.append(offer_type)
            return
        if product is None:
            raise ValueError("O produto é obrigatório para ofertas individuais.")
        self.offers[product] = self.offer_factory.create_offer(offer_type, argument)

    def checks_out_articles_from(self, the_cart: ShoppingCart) -> Receipt:
        """Processa as compras do carrinho e retorna o recibo finalizado.

        1. Cria o recibo por meio da fábrica (ReceiptFactory).
        2. Consulta o preço unitário e calcula o valor total de cada item.
        3. Delega o cálculo das ofertas (ignorado em modo de emergência Nível 3).
        """
        receipt = self.receipt_factory.create_receipt()
        product_quantities = the_cart.items
        for product_quantity in product_quantities:
            product = product_quantity.product
            quantity = product_quantity.quantity
            unit_price = self.catalog.unit_price(product)
            price = quantity * unit_price
            receipt.add_product(product, quantity, unit_price, price)

        if not self.emergency_mode:
            the_cart.handle_offers(
                receipt, self.offers, self.catalog, self.combo_offers
            )

        return receipt

    def product_with_name(self, name: str) -> Product | None:
        """Busca um produto no catálogo pelo nome via contrato CatalogReader."""
        return self.catalog.find_product_by_name(name)
