# shared fixtures for the whole test suite, kept at the root so any future
# test folder can reuse this without copy pasting

from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
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
    # logging in is a spa route change, not a real page navigation, so
    # playwright doesnt automatically wait for it the way it would for a
    # normal page.goto. waiting for the url ourselves here means the app
    # has actually finished switching to the inventory page before any
    # test starts touching it, instead of maybe catching it mid switch
    expect(login_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
    return InventoryPage(login_page.page)


@pytest.fixture()
def cart_page(page):
    return CartPage(page)


@pytest.fixture()
def checkout_page(page):
    return CheckoutPage(page)
