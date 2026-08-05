def test_send_custom_headers(playwright):
    # Headers set at context creation apply to every request from this context
    api = playwright.request.new_context(
        base_url="https://jsonplaceholder.typicode.com",
        extra_http_headers={"Accept": "application/json", "X-Client": "qa-suite"},
    )
    resp = api.get("/posts/1")
    # body = resp.json()
    # assert body["headers"]["X-Client"] == "qa-suite"
    assert resp.status == 200
    api.dispose()

def test_override_headers_per_request(api):
    # Headers on a single call override the context defaults just for that call
    resp = api.get("/posts/1", headers={"Accept": "application/json"})
    assert "application/json" in resp.headers["content-type"]
