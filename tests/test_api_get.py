def test_get_single_post(playwright):
    api = playwright.request.new_context(base_url="https://jsonplaceholder.typicode.com")
    resp = api.get("/posts/1")
    assert resp.status == 200
    assert "application/json" in resp.headers["content-type"]

    body = resp.json()
    assert set(body.keys()) == {"userId", "id", "title", "body"}
    assert isinstance(body["id"], int)
    assert body["userId"] == 1
    assert isinstance(body["title"], str)
    assert isinstance(body["body"], str)

    api.dispose()


# tests/test_api_get.py  (rewritten to use the fixture)
def test_get_single_post_with_fixture(api):
    resp = api.get("/posts/1")
    assert resp.status == 200
    assert api.get("/posts/1").json()["id"] == 1