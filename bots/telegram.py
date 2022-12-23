import os

from telethon import TelegramClient, events

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')

client = TelegramClient('sesion name', api_id, api_hash)
phone = os.getenv('TELEGRAM_PHONE')
client.start(phone=lambda: phone)

chat_pars = []

for dialog in client.iter_dialogs():
    print(dialog)


@client.on(events.NewMessage(chats=(chat_pars)))
async def normal_handler(event):
    ness_date = event.message.to_dict()['date']
    ness_id = event.message.to_dict()['id']
    print(event.message.to_dict()['message'])
    print(event.message.to_dict()['username'])
    print(ness_date, ness_id)
    print('-----------------------------------------------------------------')

    if event.photo:
        await event.download_media('img')


client.run_until_disconnected()
