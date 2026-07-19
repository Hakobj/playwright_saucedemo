# smoke_test.py
def test_title(page):
    page.goto("https://www.saucedemo.com/")
    assert "Swag Labs" in page.title()