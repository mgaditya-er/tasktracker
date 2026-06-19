import pytest

def create_user(client):
    response = client.post(
        "/users",
        json={
            "name": "Task Owner",
            "email": "owner@test.com"
        }
    )

    assert response.status_code == 201
    return response.json()


def create_task(client, owner_id):
    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Task description",
            "owner_id": owner_id
        }
    )

    assert response.status_code == 201
    return response


def test_create_task(client):

    user = create_user(client)

    response = create_task(client, user["id"])

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["owner_id"] == user["id"]


def test_create_task_invalid_owner(client):

    response = client.post(
        "/tasks",
        json={
            "title": "Invalid Task",
            "description": "No owner",
            "owner_id": 99999
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Owner not found"


def test_get_tasks(client):

    user = create_user(client)
    create_task(client, user["id"])

    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task_by_id(client):

    user = create_user(client)
    task = create_task(client, user["id"]).json()

    response = client.get(f"/tasks/{task['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == task["id"]


def test_get_task_not_found(client):

    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task_invalid_status(client):

    user = create_user(client)
    task = create_task(client, user["id"]).json()

    response = client.put(
        f"/tasks/{task['id']}",
        json={
            "status": "wrong_status"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid task status"


def test_delete_task(client):

    user = create_user(client)
    task = create_task(client, user["id"]).json()

    response = client.delete(f"/tasks/{task['id']}")

    assert response.status_code == 204