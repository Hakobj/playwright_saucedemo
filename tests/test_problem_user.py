import pytest

# This file-level fixture OVERRIDES the global browser_context_args from Step 5
# for every test in this file — pytest uses the closest fixture by name. These
# tests always run as problem_user, so we don't need the no_auth branch here.
@pytest.fixture
def browser_context_args(browser_context_args, problem_auth):
    return {**browser_context_args, "storage_state": problem_auth}

def test_problem_user_sees_broken_images(inventory_page, base_url):
    inventory_page.page.goto(base_url + "inventory.html")
    assert inventory_page.is_loaded()
    # problem_user is *designed* to misbehave — that misbehavior is what you assert on