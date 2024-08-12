
from telethon import TelegramClient

class ClientModel:

    def __init__(self):
        self.api_id = 22854449
        self.api_hash = '9620e2ba5d37da78fb24067d5e850c3b'

    def get_client(self, phone):
        return TelegramClient(f'sessions/{phone}.session', self.api_id, self.api_hash)
        