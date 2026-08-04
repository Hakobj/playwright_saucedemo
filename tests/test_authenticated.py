import pytest

#If we use @pytest.mark.no_auth - # shuould fail as we are not logged in
def test_lands_authenticated(inventory_page, base_url):
    inventory_page.page.goto(base_url+"inventory.html")
    assert inventory_page.is_loaded()