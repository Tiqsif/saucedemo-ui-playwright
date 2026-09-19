# page object for the login screen, only this file knows the actual
# locators, everything else (tests, other pages) just calls methods on this
# and doesnt care how the login form is built

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "/"  # login page is just the sites root, no separate path

    def __init__(self, page: Page):
        super().__init__(page)
        # saucedemo puts data-test attributes on basically everything, which
        # is way more stable to select on than a css class, a redesign can
        # change classes/colors without breaking these
        self.username_input = page.locator("[data-test='username']")
        self.password_input = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-button']")
        self.error_message = page.locator("[data-test='error']")

    def load(self) -> None:
        self.goto(self.URL)

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()  # on success this redirects to /inventory.html by itself

    def get_error_text(self) -> str:
        return self.error_message.inner_text()  # only call this after a login that should fail
