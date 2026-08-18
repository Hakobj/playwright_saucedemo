def test_create_post(api):
    resp = api.post("/posts", data={"userID":123, "id": 42, "title": "Senior QA engineer", "body": "learning"})
    created = resp.json()
    assert resp.status == 201
    assert created["title"] == "Senior QA engineer"
    assert "id" in created

def test_update_post(api):
    resp = api.put("/posts/1", data={"title": "changed", "body": "x", "userId": 1})
    assert resp.status == 200
    assert resp.json()["title"] == "changed"

def test_delete_post(api):
    resp = api.delete("/posts/1")
    assert resp.status == 200                        # some APIs return 204 No Content — know which

def test_missing_post_is_404(api):
    resp = api.get("/posts/99999")
    assert resp.status == 404                        # the negative case matters as much as the happy one
