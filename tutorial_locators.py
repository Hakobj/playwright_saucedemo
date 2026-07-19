#tutorial_locators.py
def test_locator_style(page):
    page.goto("https://www.saucedemo.com/")
    # 1. BRITTLE — absolute-ish CSS tied to layout / nth position
    page.locator("div.form_group:nth-child(1) > input").fill("standard_user")
    page.locator("#user-name").clear()

    # 2. OK — id selector (stable unless a dev renames the id)
    page.locator("#user-name").fill("standard_user")
    page.locator("#user-name").clear()

     # 3. BETTER — test-id attribute (exists specifically so tests can hook in)
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='username']").clear()