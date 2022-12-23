from sqlmodel import Session
from fastapi.testclient import TestClient
from db.models import User
from db.models.type_messenger import EnumTypeMessenger
from tests.utils import create_messenger, create_user, create_phone
from tests.utils.fixturies import *

url = "/messengers/telegram/"


def test_delete_telegram(session: Session, client: TestClient):
    messenger = create_messenger(session, type_id=EnumTypeMessenger.telegram)
    assert session.get(User, messenger.id) is not None
    response = client.delete(url + str(messenger.id))
    assert response.status_code == 200
    assert session.get(User, messenger.id) is None


def test_create_telegram(session: Session, client: TestClient):
    user = create_user(session)
    phone = create_phone()
    secret = {
        "api_id": 123,
        "api_hash": "api_hash"
    }
    response = client.post(url,
                           json={
                               "phone": phone,
                               "owner_id": user.id,
                               "secret": secret
                           })
    data = response.json()
    assert data["id"] is not None
    assert data["phone"] == phone


def test_patch_telegram(session: Session, client: TestClient):
    telegram = create_messenger(session, type_id=EnumTypeMessenger.telegram)
    new_phone = create_phone()
    response = client.patch(url + str(telegram.id),
                            json={
                                "phone": new_phone
                            })
    assert response.status_code == 200
    assert response.json()["phone"] == new_phone
