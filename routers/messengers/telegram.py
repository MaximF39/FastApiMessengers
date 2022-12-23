from fastapi import APIRouter, Depends
from sqlmodel import Session
from starlette.background import BackgroundTasks

from db.crud import CRUD
from db.models.type_messenger import EnumTypeMessenger
from dependencies import get_session
from logic.telegram import Telegram
from logic.telegram import TelegramCreate, TelegramUpdate, Messenger, TelegramRead

router = APIRouter(prefix="/telegram",
                   tags=["telegram"])


@router.get("/", response_model=list[TelegramRead])
def read_messengers(session: Session = Depends(get_session)):
    return CRUD.get_all(Telegram, session)


@router.post("/", response_model=TelegramRead, description="Telegram: api_token(api_hash)")
def create_messenger(messenger: TelegramCreate, session: Session = Depends(get_session)):
    messenger = Messenger(owner_id=messenger.owner_id,
                          phone=messenger.phone,
                          type_id=int(EnumTypeMessenger.telegram),
                          secret=messenger.secret.json())
    response_telegram = CRUD.create(Messenger, session, messenger)
    telegram = Telegram.from_orm(response_telegram)
    telegram.send_code()
    return response_telegram


@router.post("/{messenger_id}/send_code")
def send_code(messenger_id: int, session: Session = Depends(get_session)):
    telegram = session.get(Telegram, messenger_id)
    telegram.send_code()
    return {"ok": True}


@router.get("/{messenger_id}", response_model=TelegramRead)
def read_messenger(messenger_id: int, session: Session = Depends(get_session)):
    return CRUD.get_id(Telegram, session, messenger_id)


@router.patch("/{messenger_id}", response_model=TelegramRead)
def patch_messenger(messenger_id: int, messenger: TelegramUpdate, session: Session = Depends(get_session)):
    return CRUD.patch(Telegram, session, messenger_id, messenger)


@router.delete("/{messenger_id}", response_model=TelegramRead)
def delete_messenger(messenger_id: int, session: Session = Depends(get_session)):
    return CRUD.delete(Telegram, session, messenger_id)


@router.post("/{messenger_id}/code")
def read_code(messenger_id: int, code: str, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    telegram = session.get(Telegram, messenger_id)
    is_active = telegram.get_code(code)
    if telegram != is_active:
        telegram.is_active = is_active
        session.add(telegram)
        session.commit()
    if is_active:
        background_tasks.add_task(telegram.start, session)
    return {"result": is_active}
