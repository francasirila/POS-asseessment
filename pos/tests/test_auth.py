def test_register_login_and_read_profile(client):
    payload = {
        "username": "john",
        "email": "john@example.com",
        "password": "Password123!",
    }
    register_response = client.post("/users/register", json=payload)
    assert register_response.status_code == 201
    assert register_response.json()["username"] == "john"
    assert "password" not in register_response.json()

    login_response = client.post(
        "/users/login",
        json={"username": "john", "password": "Password123!"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    profile_response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert profile_response.status_code == 200
    assert profile_response.json()["username"] == "john"


def test_duplicate_username_is_rejected(client, registered_user):
    response = client.post(
        "/users/register",
        json={"username": registered_user["username"], "password": "Different123!"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"


def test_login_with_bad_password_is_rejected(client, registered_user):
    response = client.post(
        "/users/login",
        json={"username": registered_user["username"], "password": "wrong"},
    )

    assert response.status_code == 401


def test_profile_requires_authentication(client):
    response = client.get("/users/me")

    assert response.status_code == 401


def test_registration_validation_error(client):
    response = client.post("/users/register", json={"username": "missing-password"})

    assert response.status_code == 422


def test_list_users_requires_valid_token(client, auth_headers):
    unauthorized = client.get("/users")
    authorized = client.get("/users", headers=auth_headers)

    assert unauthorized.status_code == 401
    assert authorized.status_code == 200
    assert len(authorized.json()) == 1
