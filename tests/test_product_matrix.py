import pytest
from data.test_data import BACKPACK, BIKE_LIGHT

@pytest.mark.parametrize("product", [BACKPACK, BIKE_LIGHT])
def test_add_single_product(inventory_page, base_url, product):
    inventory_page.page.goto(base_url + "inventory.html")   # already logged in via storageState
    inventory_page.add_product(product)
    assert inventory_page.cart_count() == 1