# every page object inherits from this one, keeps stuff thats shared across
# all pages, right now just goto, in one place instead of copy pasting it into
# every single page class

from __future__ import annotations

from playwright.sync_api import Page

# pytest-playwrights own base_url ini setting turned out to not be reliable
# once xdist and multiple browsers are both running at once, some workers
# just never got it applied and tried to navigate to a bare "/", which
# isnt a real url on its own. building the full url ourselves here means
# it always works the same way no matter how the suite gets run
BASE_URL = "https://www.saucedemo.com"


class BasePage:
    def __init__(self, page: Page):
        self.page = page  # the actual playwright page were driving around

    def goto(self, path: str = "/") -> None:
        self.page.goto(f"{BASE_URL}{path}")
