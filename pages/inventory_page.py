# pages/inventory_page.py
class InventoryPage:
    def __init__(self, page):
        self.page = page
        # LOCATORS
        self.title      = page.locator(".title")                  # "Products" header
        self.cart_badge = page.locator(".shopping_cart_badge")    # the little count bubble
        self.cart_link  = page.locator(".shopping_cart_link")

    # ACTIONS
    def add_item_to_cart(self, item_name):
        # saucedemo builds these ids like: add-to-cart-sauce-labs-backpack
        slug = item_name.lower().replace(" ", "-")
        self.page.locator(f"[data-test='add-to-cart-{slug}']").click()

    def open_cart(self):
        self.cart_link.click()

    # QUERIES — questions the test can ask, phrased in domain language.
    def is_loaded(self):
        return self.title.inner_text() == "Products"

    def cart_count(self):
        if self.cart_badge.count() == 0:
            return 0                       # no badge shows when cart is empty
        return int(self.cart_badge.inner_text())

    def add_product(self, product):    # product is a Product dataclass
        slug = product.name.lower().replace(" ", "-")
        self.page.locator(f"[data-test='add-to-cart-{slug}']").click()

