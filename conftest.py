import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@pytest.fixture
def login_page(page):                # depends on the built-in 'page' fixture
    return LoginPage(page)

@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)


from data.models import User


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
