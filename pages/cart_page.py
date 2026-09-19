# page object for the cart screen, saucedemo just calls the path cart.html

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    URL = "/cart.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.item_names = page.locator("[data-test='inventory-item-name']")
        self.checkout_button = page.locator("[data-test='checkout']")

    def load(self) -> None:
        self.goto(self.URL)

    def get_item_names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def remove_item(self, item_slug: str) -> None:
        # same naming pattern as the inventory page, remove-<slug>
        self.page.locator(f"[data-test='remove-{item_slug}']").click()

    def go_to_checkout(self) -> None:
        self.checkout_button.click()
