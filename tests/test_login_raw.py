# tests/test_login_raw.py  (this is the BEFORE — we won't keep it)
def test_valid_login_raw_witout_pom(page):
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()
    assert page.locator(".title").inner_text() == "Products"
