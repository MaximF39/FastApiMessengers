from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.crud import CRUD
from db.models import Chat, Messenger
from db.models.chat import ChatCreate, ChatRead
from dependencies import get_session

router = APIRouter(prefix="/chats", tags=["chat"])


@router.get("/{messenger_id}/all", response_model=list[ChatRead])
def read_free_chats(messenger_id: int, session: Session = Depends(get_session)):
    messenger = session.get(Messenger, messenger_id)
    messenger = messenger.factory()
    return list(messenger.chats())


@router.get("/{messenger_id}", response_model=list[ChatRead])
def get_chats(messenger_id: int, session: Session = Depends(get_session)):
    messenger = session.get(Messenger, messenger_id)
    chats = messenger.chats
    return chats


@router.post("/", response_model=ChatRead)
def create_chat(chat: ChatCreate, session: Session = Depends(get_session)):
    return CRUD.create(Chat, session, chat)


@router.delete("/{chat_id}", response_model=ChatRead)
def delete_chat(chat_id: int, session: Session = Depends(get_session)):
    return CRUD.delete(Chat, session, chat_id)
