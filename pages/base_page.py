# every page object inherits from this one, keeps stuff thats shared across
# all pages, right now just goto, in one place instead of copy pasting it into
# every single page class

from __future__ import annotations

from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page  # the actual playwright page were driving around

    def goto(self, path: str = "/") -> None:
        # path is relative on purpose, base_url lives in pytest.ini, so this
        # actually becomes https://www.saucedemo.com + whatever path we pass
        self.page.goto(path)
