import pytest
import os
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from data.test_data import STANDARD_USER, PROBLEM_USER
from data.models import User

AUTH_FILE = ".auth/standard.json"

@pytest.fixture
def login_page(page):                # depends on the built-in 'page' fixture
    return LoginPage(page)

@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)



# We are using a demo website so they’re all going to be saucedemo, but 
# this should still drive home the point.
ENVIRONMENTS = {
    "dev":     {"base_url": "https://www.saucedemo.com/", "user": User("standard_user", "secret_sauce")},
    "staging": {"base_url": "https://www.saucedemo.com/", "user": User("standard_user", "secret_sauce")},
    "prod":    {"base_url": "https://www.saucedemo.com/", "user": User("standard_user", "secret_sauce")},
}

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev",
                     help="Target environment: dev | staging | prod")

@pytest.fixture(scope="session")
def env_config(request):
    env_name = request.config.getoption("--env")
    config = ENVIRONMENTS[env_name]
    print(f"\n>>> Running against: {env_name} ({config['base_url']})")
    return config

@pytest.fixture(scope="session")
def base_url(env_config):
    return env_config["base_url"]


@pytest.fixture(scope="session")
def base_url_session(request):
    env_name = request.config.getoption("--env")
    return ENVIRONMENTS[env_name]["base_url"]

@pytest.fixture(scope="session")
def standard_auth_state(browser_type, base_url_session):
    """Log in once per test run, save the session, hand back the path."""
    os.makedirs(".auth", exist_ok=True)

    if os.path.exists(AUTH_FILE):
        return AUTH_FILE

    browser = browser_type.launch()
    page = browser.new_page()
    page.goto(base_url_session)
    page.fill("[data-test='username']", STANDARD_USER.username)
    page.fill("[data-test='password']", STANDARD_USER.password)
    page.click("[data-test='login-button']")
    page.wait_for_url("**/inventory.html")
    page.context.storage_state(path=AUTH_FILE)
    browser.close()

    return AUTH_FILE

@pytest.fixture
def browser_context_args(browser_context_args, request, standard_auth_state):
    # A test marked @pytest.mark.no_auth gets a clean, logged-OUT browser.
    if request.node.get_closest_marker("no_auth"):
        return browser_context_args
    return {**browser_context_args, "storage_state": standard_auth_state}


def pytest_configure(config):
    config.addinivalue_line("markers", "no_auth: start with a clean, logged-out browser")


def _make_auth_state(browser_type, base_url, user, filename):
    path = f".auth/{filename}"
    if os.path.exists(path):
        return path

    browser = browser_type.launch()
    page = browser.new_page()
    page.goto(base_url)
    page.fill("[data-test='username']", user.username)
    page.fill("[data-test='password']", user.password)
    page.click("[data-test='login-button']")
    page.wait_for_url("**/inventory.html")
    page.context.storage_state(path=path)
    browser.close()
    return path

@pytest.fixture(scope="session")
def standard_auth(browser_type, base_url_session):
    return _make_auth_state(browser_type, base_url_session, STANDARD_USER, "standard.json")

@pytest.fixture(scope="session")
def problem_auth(browser_type, base_url_session):
    return _make_auth_state(browser_type, base_url_session, PROBLEM_USER, "problem.json")


