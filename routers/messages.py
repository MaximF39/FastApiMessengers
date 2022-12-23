from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from db.models import Message
from db.models.message import MessageWithFiles
from dependencies import get_session

router = APIRouter(prefix="/messages", tags=["message"])


@router.get("/{chat_id}", response_model=list[MessageWithFiles])
def read_messages(chat_id: int, count: int = 10, skip: int = 0, session: Session = Depends(get_session)):
    stmt = select(Message).where(Message.chat_id == chat_id).limit(count).offset(skip)
    messages = session.exec(stmt).all()
    return messages
