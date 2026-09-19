# page object for the product listing, this is the page you land on right
# after logging in, and where add to cart actually happens

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class InventoryPage(BasePage):
    URL = "/inventory.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")
        self.cart_link = page.locator("[data-test='shopping-cart-link']")

    def load(self) -> None:
        self.goto(self.URL)

    def add_to_cart(self, item_slug: str) -> None:
        # every add to cart button is named add-to-cart-<the items slug>,
        # so one locator built from the slug works for any product
        self.page.locator(f"[data-test='add-to-cart-{item_slug}']").click()

    def remove_from_cart(self, item_slug: str) -> None:
        # the same button turns into remove-<slug> once the item is in the cart
        self.page.locator(f"[data-test='remove-{item_slug}']").click()

    def get_cart_count(self) -> int:
        # the badge element doesnt exist at all when the cart is empty, it
        # only shows up once theres at least 1 item, so check count() first
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.inner_text())

    def go_to_cart(self) -> None:
        self.cart_link.click()
