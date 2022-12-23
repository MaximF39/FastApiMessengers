from fastapi.testclient import TestClient
from sqlmodel import Session
from tests.utils.fixturies import *

from tests.utils import create_message, create_chat, create_file

url = "/messages"


def test_read_messages_with_files(session: Session, client: TestClient):
    chat = create_chat(session)
    message1 = create_message(session, chat_id=chat.id)
    file = create_file(session, message_id=message1.id)
    message2 = create_message(session, chat_id=chat.id)

    response = client.get(url + f"/{chat.id}")
    data = response.json()

    assert len(data) == 2
    assert data[0]["id"] == message1.id
    assert data[0]["chat_id"] == chat.id
    assert len(data[0]["files"]) == 1
    assert data[0]["files"][0]["id"] == file.id
    assert data[1]["id"] == message2.id
    assert data[1]["chat_id"] == chat.id
    assert len(data[1]["files"]) == 0
