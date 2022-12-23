import uvicorn
from fastapi import FastAPI

from db.db import create_db_and_tables
from routers import users, messengers, messages, chats

app = FastAPI(title="Документация",
              description=("Документация для получения сообщений, добавление чатов и мессенджеров. "
                           "Telegram: **@maxf39**"),
              version="0.0.1",
              contact={
                  "name": "Maxim Fedotov",
                  "Telegram": "@maxf39",
                  "GitHub": "https://github.com/MaximF39"
              })

app.include_router(users.router)
app.include_router(messengers.router)
app.include_router(chats.router)
app.include_router(messages.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    #migrate_db()


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
