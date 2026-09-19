# cart tests build on top of inventory_page, which already logs in and
# lands on the product listing, so none of these repeat any login code

from __future__ import annotations

BACKPACK = "sauce-labs-backpack"
BIKE_LIGHT = "sauce-labs-bike-light"


def test_add_item_shows_up_in_cart(inventory_page, cart_page):
    inventory_page.add_to_cart(BACKPACK)
    assert inventory_page.get_cart_count() == 1

    inventory_page.go_to_cart()
    assert "Sauce Labs Backpack" in cart_page.get_item_names()


def test_add_two_items_updates_badge_count(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)
    assert inventory_page.get_cart_count() == 2


def test_remove_item_from_inventory_page(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.remove_from_cart(BACKPACK)
    # the badge disappears completely once the cart goes back to empty
    assert inventory_page.get_cart_count() == 0


def test_remove_item_from_cart_page(inventory_page, cart_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.go_to_cart()

    cart_page.remove_item(BACKPACK)
    assert cart_page.get_item_names() == []
