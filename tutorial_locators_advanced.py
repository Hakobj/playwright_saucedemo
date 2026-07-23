def test_locators_relationship(page):
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()

    # Get 6 onventory items
    items = page.locator(".inventory_item")
    print("\nFound {} items on the page".format(items.count()))
    backpack = page.locator(".inventory_item").filter(has_text="Backpack")
    print("Backpack locator is:", backpack)

    # CHAIN — from that card, drill INTO its button (scoped to the card, not the page)
    backpack.get_by_role("button", name="Add to cart").click()

    # Find price
    price = (page.locator(".inventory_item")
             .filter(has_text="Backpack")
             .locator(".inventory_item_price"))
    print("\nPrice of backpack is: ", price.inner_text())


def test_strictnes(page):
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()

    # This matches 6 buttons -> Playwright REFUSES to act (strict mode violation)
    page.get_by_role("button", name="Add to cart").click()   
    # will error as strict mode violation as there are multiple roles having "button"