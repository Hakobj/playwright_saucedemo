# # tests/test_login.py  (this is the AFTER — keep this)
# from pages.login_page import LoginPage
# from pages.inventory_page import InventoryPage

# def test_valid_login(page):
#     login = LoginPage(page)                     # 1. wrap the page in the object
#     login.goto("https://www.saucedemo.com/")    #    (base_url comes from a fixture in Part 3)
#     login.login("standard_user", "secret_sauce")# 2. do the action, no selectors in sight

#     inventory = InventoryPage(page)             # 3. we're on a new screen -> new page object
#     assert inventory.is_loaded()                # 4. the TEST makes the judgment call


# tests/test_login.py  (upgraded — no more manual LoginPage(page))
from data.test_data import STANDARD_USER

def test_valid_login(login_page, inventory_page, base_url, env_config):     # <- fixtures injected by name
    login_page.goto(base_url)
    login_page.login_as(env_config["user"])

    assert inventory_page.is_loaded()

