import pytest

def test_register_and_login(client):
    # 1. Register
    reg_payload = {
        "email": "testcandidate@example.com",
        "password": "SecurePassword123!",
        "full_name": "Test Candidate"
    }
    res_reg = client.post("/api/auth/register", json=reg_payload)
    assert res_reg.status_code == 201
    data = res_reg.json()
    assert "access_token" in data
    assert data["user"]["email"] == "testcandidate@example.com"
    assert data["user"]["full_name"] == "Test Candidate"

    # 2. Duplicate registration check
    res_dup = client.post("/api/auth/register", json=reg_payload)
    assert res_dup.status_code == 400

    # 3. Login
    login_payload = {
        "email": "testcandidate@example.com",
        "password": "SecurePassword123!"
    }
    res_login = client.post("/api/auth/login", json=login_payload)
    assert res_login.status_code == 200
    token = res_login.json()["access_token"]

    # 4. Access /me with token
    headers = {"Authorization": f"Bearer {token}"}
    res_me = client.get("/api/auth/me", headers=headers)
    assert res_me.status_code == 200
    assert res_me.json()["email"] == "testcandidate@example.com"

def test_invalid_login(client):
    res = client.post("/api/auth/login", json={"email": "nonexistent@example.com", "password": "wrong"})
    assert res.status_code == 401
