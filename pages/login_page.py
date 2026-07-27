# pages/login_page.py

class LoginPage:
    # The URL path this page lives at. Kept here so the test never hardcodes it.
    PATH = ""   # saucedemo login is the root "/"

    def __init__(self, page):
        self.page = page
        # LOCATORS — every element this page cares about, named once, in one place.
        self.username   = page.locator("[data-test='username']")
        self.password   = page.locator("[data-test='password']")
        self.login_btn  = page.locator("[data-test='login-button']")
        self.error_msg  = page.locator("[data-test='error']")

    # ACTIONS — verbs a user can perform on this screen.
    def goto(self, base_url):
        self.page.goto(base_url + self.PATH)

    def login(self, user, pwd):
        self.username.fill(user)
        self.password.fill(pwd)
        self.login_btn.click()

    # A small query helper — lets the TEST ask a question without knowing the selector.
    def error_text(self):
        return self.error_msg.inner_text()

    def login_as(self, user):          # user is a User dataclass
        self.username.fill(user.username)
        self.password.fill(user.password)
        self.login_btn.click()


