from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from data.test_data import STANDARD_USER, BACKPACK, BIKE_LIGHT

def test_add_two_items_updates_cart(page):
    login = LoginPage(page)
    login.goto("https://www.saucedemo.com/")
    login.login_as(STANDARD_USER)               # <- no raw credentials

    inventory = InventoryPage(page)
    assert inventory.cart_count() == 0

    inventory.add_product(BACKPACK)             # <- no magic strings
    inventory.add_product(BIKE_LIGHT)

    assert inventory.cart_count() == 2
