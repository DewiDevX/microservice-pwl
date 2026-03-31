def test_create_item_success(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/items/", json={
        "title": "Test Item",
        "description": "This is a test item"
    }, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Item"
    assert data["description"] == "This is a test item"
    assert "id" in data

def test_create_item_unauthorized(client):
    response = client.post("/items/", json={
        "title": "No Auth Item",
        "description": "Should fail"
    })
    assert response.status_code == 401

def test_read_items(client, user_token, db):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get("/items/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_single_item(client, user_token, db):
    # Create item first
    headers = {"Authorization": f"Bearer {user_token}"}
    create_resp = client.post("/items/", json={
        "title": "Single Item",
        "description": "For detail test"
    }, headers=headers)
    item_id = create_resp.json()["id"]
    
    response = client.get(f"/items/{item_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Single Item"

def test_update_item_success(client, user_token, db):
    headers = {"Authorization": f"Bearer {user_token}"}
    # Create item
    create_resp = client.post("/items/", json={
        "title": "Old Title",
        "description": "Old Desc"
    }, headers=headers)
    item_id = create_resp.json()["id"]
    
    # Update item
    update_resp = client.put(f"/items/{item_id}", json={
        "title": "New Title",
        "description": "New Desc"
    }, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "New Title"

def test_delete_item_success(client, user_token, db):
    headers = {"Authorization": f"Bearer {user_token}"}
    create_resp = client.post("/items/", json={
        "title": "To Be Deleted",
        "description": "Will be removed"
    }, headers=headers)
    item_id = create_resp.json()["id"]
    
    delete_resp = client.delete(f"/items/{item_id}", headers=headers)
    assert delete_resp.status_code == 204
    
    get_resp = client.get(f"/items/{item_id}", headers=headers)
    assert get_resp.status_code == 404