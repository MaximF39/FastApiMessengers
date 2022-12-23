from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from starlette.background import BackgroundTasks

from db.crud import CRUD
from db.models.messenger import MessengerRead, Messenger
from db.models.type_messenger import EnumTypeMessenger
from dependencies import get_session
from logic.whatsapp import WhatsappRead, Whatsapp, WhatsappCreate, WhatsappUpdate

router = APIRouter(prefix="/whatsapp",
                   tags=["whatsapp"])


@router.get("/", response_model=list[WhatsappRead])
def read_messengers(session: Session = Depends(get_session)):
    return CRUD.get_all(Whatsapp, session)


@router.post("/", response_model=MessengerRead,
             description="Telegram: api_token(api_hash)")
def create_messenger(messenger: WhatsappCreate, session: Session = Depends(get_session)):
    messenger = Messenger(owner_id=messenger.owner_id,
                          phone=messenger.phone,
                          type_id=int(EnumTypeMessenger.whatsapp),
                          secret=messenger.secret.json())
    response_whatsapp = CRUD.create(Messenger, session, messenger)
    whatsapp = Whatsapp.from_orm(response_whatsapp)
    whatsapp.send_code()
    return response_whatsapp


@router.get("/{messenger_id}", response_model=MessengerRead)
def read_messenger(messenger_id: int, session: Session = Depends(get_session)):
    return CRUD.get_id(Whatsapp, session, messenger_id)


@router.patch("/{messenger_id}", response_model=WhatsappRead)
def patch_messenger(messenger_id: int, messenger: WhatsappUpdate, session: Session = Depends(get_session)):
    return CRUD.patch(Whatsapp, session, messenger_id, messenger)


@router.delete("/{messenger_id}", response_model=WhatsappRead)
def delete_messenger(messenger_id: int, session: Session = Depends(get_session)):
    return CRUD.delete(Whatsapp, session, messenger_id)


@router.post("/{messenger_id}/send_code")
def send_code(messenger_id: int, session: Session = Depends(get_session)):
    whatsapp = session.get(Whatsapp, messenger_id)
    whatsapp.send_code()
    return {"ok": True}


@router.post("/{messenger_id}/code")
def read_code(messenger_id: int, code: str, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    whatsapp = session.get(Whatsapp, messenger_id)
    is_active = whatsapp.get_code(code)
    if whatsapp != is_active:
        whatsapp.is_active = is_active
        session.add(whatsapp)
        session.commit()
    if is_active:
        background_tasks.add_task(whatsapp.start, session)
    return {"result": is_active}
