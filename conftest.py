# shared fixtures for the whole test suite, same idea as the conftest in
# qa-automation-utils, keep it at the root so any future test folder can
# reuse this without copy pasting

from __future__ import annotations

import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

# saucedemo lists these accounts right on the login page itself, not a secret
STANDARD_USER = "standard_user"
LOCKED_OUT_USER = "locked_out_user"
PASSWORD = "secret_sauce"


@pytest.fixture()
def login_page(page):
    # "page" here comes from the pytest-playwright plugin, it already spins
    # up a browser + fresh page for every test, we dont manage that ourselves
    lp = LoginPage(page)
    lp.load()  # every test that asks for this fixture starts on a loaded login page
    return lp


@pytest.fixture()
def inventory_page(login_page):
    # cart and checkout tests all need to start logged in, doing the login
    # here means those tests dont repeat login code themselves
    login_page.login(STANDARD_USER, PASSWORD)
    return InventoryPage(login_page.page)


@pytest.fixture()
def cart_page(page):
    return CartPage(page)
