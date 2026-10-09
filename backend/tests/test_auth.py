
def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "login": "newuser",
            "email": "newuser@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["login"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "password_hash" not in data


def test_login_success(client, create_user):
    user = create_user()

    response = client.post(
        "/auth/login",
        json={
            "email": user["payload"]["email"],
            "password": user["payload"]["password"],
        },
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_login_wrong_password(client, create_user):
    user = create_user()

    response = client.post(
        "/auth/login",
        json={
            "email": user["payload"]["email"],
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401


def test_login_unknown_email(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "SomePassword123!",
        },
    )

    assert response.status_code == 401


def test_get_me_with_token(client, create_user):
    user = create_user()

    response = client.get(
        "/auth/me",
        headers=user["headers"],
    )

    assert response.status_code == 200
    assert response.json()["email"] == user["payload"]["email"]


def test_get_me_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_get_me_with_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401