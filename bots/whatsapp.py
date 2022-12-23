import os
from pprint import pprint

import requests

token_api = os.getenv("WHATSAPP_TOKEN_API")
url = "https://wappi.pro"
headers = {"Authorization": token_api}

message_url_get = "/api/sync/messages/get"


def messages(limit=10):
    params = {
        "profile_id": os.getenv("WHATSAPP_PROFILE_ID"),
        "chat_id": os.getenv("WHATSAPP_CHAT_ID"),
        "limit": limit
    }

    full_url = url + message_url_get

    response = requests.get(full_url, headers=headers, params=params)
    return response.json()



pprint(messages())
