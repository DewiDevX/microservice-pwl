def test_admin_can_access_admin_endpoint(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/admin/users", headers=headers)
    assert response.status_code == 200

def test_user_cannot_access_admin_endpoint(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get("/admin/users", headers=headers)
    assert response.status_code == 403
    assert "Not enough permissions" in response.json()["detail"]

def test_user_can_only_update_own_item(client, user_token, test_user, db):
    headers = {"Authorization": f"Bearer {user_token}"}
    
    # Create item owned by test_user
    create_resp = client.post("/items/", json={
        "title": "User's Item",
        "description": "Owned by user"
    }, headers=headers)
    item_id = create_resp.json()["id"]
    
    # Try to update with another user's token (simulate different user)
    # Create second user
    client.post("/auth/register", json={
        "username": "otheruser",
        "email": "other@example.com",
        "password": "otherpass"
    })
    login_resp = client.post("/auth/login", data={   # <- data, not json
        "username": "otheruser",
        "password": "otherpass"
    })
    other_token = login_resp.json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}
    
    # Other user tries to update first user's item
    update_resp = client.put(f"/items/{item_id}", json={
        "title": "Hacked Title"
    }, headers=other_headers)
    
    assert update_resp.status_code == 403
    assert "Access denied" in update_resp.json()["detail"]

def test_admin_can_update_any_item(client, admin_token, user_token, test_user, db):
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    user_headers = {"Authorization": f"Bearer {user_token}"}
    
    # User creates item
    create_resp = client.post("/items/", json={
        "title": "Admin Test Item",
        "description": "Will be updated by admin"
    }, headers=user_headers)
    item_id = create_resp.json()["id"]
    
    # Admin updates user's item
    update_resp = client.put(f"/items/{item_id}", json={
        "title": "Updated by Admin",
        "description": "Admin override"
    }, headers=admin_headers)
    
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "Updated by Admin"