# one full path through checkout, cart to info to overview to done, all
# in a single test since its really one flow, not separate features

from __future__ import annotations

BACKPACK = "sauce-labs-backpack"


def test_full_checkout_flow(inventory_page, cart_page, checkout_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.go_to_cart()

    cart_page.go_to_checkout()
    checkout_page.fill_info("Emre", "Test", "12345")

    # the backpack is $29.99 on the real site, plus tax that comes out to
    # $32.39, checking the actual math instead of just checking a button exists
    assert "32.39" in checkout_page.get_total_text()

    checkout_page.finish()
    assert "Thank you for your order" in checkout_page.get_confirmation_text()
