"""
A very simple telegram bot messenger
"""
import requests
import json


class Message:
    def __init__(self, message_id: int):
        self.message_id = message_id


class Bot:
    def __init__(self, token: str):
        self.base_url = f"https://api.telegram.org/bot{token}/"

    def send_message(self, chat_id: str, text: str):
        url = self.base_url + "sendMessage"

        data = {
            'text': (None, text),
            'chat_id': (None, int(chat_id)),
            'parse_mode': (None, 'HTML')
        }

        # Send
        response = requests.post(url=url, headers={}, files=data)
        res = json.loads(response.text.encode("utf-8"))
        msg = Message(res["result"]["message_id"])
        return msg

