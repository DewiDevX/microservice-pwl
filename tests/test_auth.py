def test_register_success(client):
    response = client.post("/auth/register", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "newpass123",
        "role": "user"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"
    assert "id" in data

def test_register_duplicate_username(client, test_user):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "another@example.com",
        "password": "pass123"
    })
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]

def test_login_success(client, test_user):
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client, test_user):
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "wrongpass"
    })
    assert response.status_code == 401

def test_login_nonexistent_user(client):
    response = client.post("/auth/login", data={
        "username": "nonexistent",
        "password": "anything"
    })
    assert response.status_code == 401