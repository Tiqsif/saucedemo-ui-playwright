# smallest possible slice to prove the page object pattern actually works
# end to end, just login, nothing else yet. cart/checkout tests get built
# on top of this same pattern later

from __future__ import annotations

from playwright.sync_api import expect

from conftest import LOCKED_OUT_USER, PASSWORD, STANDARD_USER


def test_valid_login_redirects_to_inventory(login_page, page):
    login_page.login(STANDARD_USER, PASSWORD)
    # saucedemo sends you here automatically once login actually works, so
    # checking the url is basically checking "did the login succeed"
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


def test_locked_out_user_shows_error(login_page):
    login_page.login(LOCKED_OUT_USER, PASSWORD)
    # exact wording straight from the site: "Epic sadface: Sorry, this user has been locked out."
    assert "locked out" in login_page.get_error_text().lower()


def test_wrong_password_shows_error(login_page):
    login_page.login(STANDARD_USER, "wrong_password")
    # exact wording: "Epic sadface: Username and password do not match any user in this service"
    assert "do not match" in login_page.get_error_text().lower()
