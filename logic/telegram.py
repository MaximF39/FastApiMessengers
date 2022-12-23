import json
from typing import Optional

from sqlmodel import Session, SQLModel
from telethon import events, TelegramClient

from db.crud import CRUD
from db.models.messenger import Messenger
from db.models.chat import ChatRead
from db.models.messenger import MessengerCreate, MessengerUpdate, MessengerRead
from db.models.type_messenger import EnumTypeMessenger
from logic.path import path_static_image


class Telegram(Messenger):

    @property
    def api_id(self):
        return self.secret_dict["api_id"]

    @property
    def api_hash(self):
        return self.secret_dict["api_hash"]

    def start(self, session: Session):
        chats = self.chats

        @self.client.on(events.NewMessage(chats=chats))
        async def normal_handler(event):
            from db.models.file import File
            from db.models.message import Message

            message = Message(
                sent_at=event.message.to_dict()['date'],
                message_id=event.message.to_dict()['id'],
                text=event.message.to_dict()['message'],
                author=event.message.to_dict()['username'],
            )
            CRUD.create(Message, session, message)
            if event.photo:
                file = await event.download_media(
                    path_static_image(EnumTypeMessenger.telegram, self.phone, self.api_id))
                # for file in files:
                file = File(path=file.path, message_id=message.id)
                CRUD.create(File, session, file, commit=False)

        self.client.run_until_disconnected()

    async def send_code(self):
        self.client.send_code_request(self.phone)

    def get_code(self, code: str):
        try:
            self.client.start(phone=lambda: self.phone, code_callback=lambda: code, max_attempts=1)
        except RuntimeError:
            result = False
        else:
            result = True
        return result

    def chats(self) -> ChatRead:
        self.check_active()
        for dialog in self.client.iter_dialogs():
            yield ChatRead(name=dialog.name,
                           chat_id=dialog.id)

    @property
    def session_name(self):
        return f'{self.phone}_{self.api_id}'

    @property
    def client(self):
        client = TelegramClient(self.session_name, self.api_id, self.api_hash)
        return client


class TelegramRead(MessengerRead):
    pass


class TelegramSecret(SQLModel):
    api_id: int
    api_hash: str


class TelegramCreate(MessengerCreate):
    secret: TelegramSecret


class TelegramUpdate(MessengerUpdate):
    secret: Optional[TelegramSecret]
