# app/settings.py
# small helper for higher-level settings management (optional)
from typing import Any
from storage import Storage

class Settings:
    def __init__(self, storage: Storage):
        self.storage = storage

    def get_threshold(self) -> float:
        return float(self.storage.get('threshold', 30.0))

    def set_threshold(self, value: float):
        self.storage.put('threshold', value)

    def get_countdown(self) -> int:
        return int(self.storage.get('countdown', 20))

    def set_countdown(self, seconds: int):
        self.storage.put('countdown', seconds)

    def get_contact(self) -> dict:
        return {
            "name": self.storage.get('contact_name', ''),
            "phone": self.storage.get('contact_phone', '')
        }
