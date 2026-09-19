# problem_user is one of saucedemos own built in test accounts, and its
# broken on purpose, sauce labs ships it specifically so people can practice
# finding bugs on it. these tests assert the correct behavior, the same
# behavior standard_user actually has, so they genuinely fail against
# problem_user, on purpose, thats not a mistake in this suite, its proof
# the bug is real. left as real failures, not xfail, specifically so the
# screenshot, video and trace on failure system actually gets exercised
# for real instead of only in theory

from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

PROBLEM_USER = "problem_user"
PASSWORD = "secret_sauce"


@pytest.fixture()
def problem_inventory_page(page):
    lp = LoginPage(page)
    lp.load()
    lp.login(PROBLEM_USER, PASSWORD)
    # same spa timing gap as the standard user fixture in conftest, login
    # is a client side route change not a real navigation, so playwright
    # wont wait for it on its own. waiting for the url means the app has
    # actually finished rendering the inventory page with problem_users
    # cookie already in effect before we touch anything on it
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    return InventoryPage(page)


def test_problem_user_product_images_are_unique(problem_inventory_page):
    # checked sauce labs own source for saucedemo, its public on github,
    # saucelabs/sample-app-web. the image override for problem_user is just
    # "if the session cookie says problem_user, use sl-404.jpg for every
    # product", a plain equality check, no randomness anywhere near it. so
    # the bug itself is actually the same every single time, not flaky on
    # sauce labs side like i first thought. the passes i saw earlier were
    # almost certainly this test reading the page mid switch, right after
    # the login redirect but before problem_users cookie driven render had
    # actually landed, which is what the url wait in the fixture above and
    # the count wait in get_image_sources are for
    sources = problem_inventory_page.get_image_sources()
    assert len(sources) == 6
    # each of the 6 products should have its own image, so 6 different
    # sources, problem_user actually returns the same one 6 times
    assert len(set(sources)) == len(sources)


def test_problem_user_sort_by_name_descending_works(problem_inventory_page):
    names_before = problem_inventory_page.get_item_names()

    problem_inventory_page.sort_by("za")
    names_after = problem_inventory_page.get_item_names()

    # switching to z to a should reverse the list, problem_user leaves it
    # exactly where it started
    assert names_after == list(reversed(names_before))
