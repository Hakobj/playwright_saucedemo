import pytest
from data.test_data import STANDARD_USER, LOCKED_OUT_USER, PROBLEM_USER

# Each tuple is (user, should_succeed). One test body, many tests.
@pytest.mark.no_auth   # <-- start logged OUT: we are testing login itself
@pytest.mark.parametrize("user,should_succeed", [
    (STANDARD_USER,   True),
    (LOCKED_OUT_USER, False),
    (PROBLEM_USER,    True),   # problem_user logs in but the UI misbehaves after
])
def test_login_outcomes(login_page, inventory_page, base_url, user, should_succeed):
    login_page.goto(base_url)
    login_page.login_as(user)
    if should_succeed:
        assert inventory_page.is_loaded()
    else:
        assert "locked out" in login_page.error_text().lower()
