import json
from datetime import datetime

from sqlmodel import Session, SQLModel

from db.models import User, Messenger, Chat, Message, File
from db.models.type_messenger import EnumTypeMessenger
from tests.utils import create_phone


def save_and_update(session: Session, model: SQLModel) -> SQLModel:
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


def create_user(session: Session, email="max", password="max", staff=None, is_blocked=False) -> SQLModel:
    user = User(email=email,
                password=password,
                staff=staff,
                is_blocked=is_blocked)
    return save_and_update(session, user)


def create_messenger(session: Session, type_id: int, owner_id=None, phone=create_phone(),
                     secret=json.dumps({"api_id": 123,
                                        "api_hash": "api_hash"})
                     ) -> SQLModel:
    if owner_id is None:
        owner_id = create_user(session).id
    messenger = Messenger(owner_id=owner_id, phone=phone,
                          secret=secret, type_id=type_id)
    return save_and_update(session, messenger)


def create_chat(session: Session, name="chat_max", chat_id="123", messenger_id=None):
    if messenger_id is None:
        messenger_id = create_messenger(session, type_id=EnumTypeMessenger.telegram).id
    chat = Chat(name=name, chat_id=chat_id, messenger_id=messenger_id)
    return save_and_update(session, chat)


def create_message(session: Session, author="max", message_id="123", text="text from max",
                   files=None, sent_at=datetime.now, chat_id=None):
    if chat_id is None:
        chat_id = create_chat(session).id
    if files is None:
        files = []
    message = Message(author=author, message_id=message_id, text=text,
                      files=files, sent_at=sent_at(), chat_id=chat_id)

    return save_and_update(session, message)


def create_file(session: Session, message_id: int, path: str = "path_max.txt", sent_at=datetime.now):
    file = File(path=path, message_id=message_id, sent_at=sent_at())
    return save_and_update(session, file)
