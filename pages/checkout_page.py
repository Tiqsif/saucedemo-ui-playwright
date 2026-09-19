# page object for the whole checkout flow, all 3 steps live in one class
# since theyre really one flow split across pages, not 3 separate features

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # step one, the info form
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.postal_code_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")

        # step two, the order overview
        self.total_label = page.locator("[data-test='total-label']")
        self.finish_button = page.locator("[data-test='finish']")

        # step three, the confirmation screen
        self.complete_header = page.locator("[data-test='complete-header']")

    def fill_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()  # this is what takes you from step one to step two

    def get_total_text(self) -> str:
        return self.total_label.inner_text()

    def finish(self) -> None:
        self.finish_button.click()  # this is what actually places the order

    def get_confirmation_text(self) -> str:
        return self.complete_header.inner_text()
