from fastapi.testclient import TestClient
from sqlmodel import Session

from db.models import User
from tests.utils import create_user


def test_create_user(client: TestClient):
    response = client.post(
        "/users/", json={"email": "max",
                         "password": "max"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["email"] == "max"
    assert not data["is_blocked"]
    assert data["id"] is not None


def test_read_users(session: Session, client: TestClient):
    user_1 = create_user(session)
    user_2 = create_user(session)
    response = client.get("/users/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["id"] == user_1.id
    assert data[0]["email"] == user_1.email
    assert data[1]["id"] == user_2.id
    assert data[1]["email"] == user_2.email


def test_read_user(session: Session, client: TestClient):
    user_1 = create_user(session)

    response = client.get(f"/users/{user_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["email"] == user_1.email
    assert data["id"] == user_1.id


def test_patch_user(session: Session, client: TestClient):
    user_1 = create_user(session)
    response = client.patch(f"/users/{user_1.id}", json={"email": "max"})
    data = response.json()

    assert response.status_code == 200
    assert data["email"] == "max"
    assert data["id"] == user_1.id


def test_delete_user(session: Session, client: TestClient):
    user_1 = create_user(session)
    response = client.delete(f"/users/{user_1.id}")
    user_in_db = session.get(User, user_1.id)
    assert response.status_code == 200
    assert user_in_db is None
