import pytest


def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "name": "Aditya",
            "email": "aditya@test.com"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "aditya@test.com"
    assert "id" in data


def test_create_user_duplicate_email(client):

    client.post(
        "/users",
        json={
            "name": "User1",
            "email": "dup@test.com"
        }
    )

    response = client.post(
        "/users",
        json={
            "name": "User2",
            "email": "dup@test.com"
        }
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"


def test_get_users(client):

    response = client.get("/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_by_id(client):

    create = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "testuser@test.com"
        }
    ).json()

    user_id = create["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_get_user_not_found(client):

    response = client.get("/users/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"