# app/storage.py
import os
from kivy.storage.jsonstore import JsonStore
from logger import get_logger

logger = get_logger(__name__)

DEFAULT_STORE = os.path.join(os.path.dirname(__file__), "..", "shock_store.json")

class Storage:
    def __init__(self, filename: str = DEFAULT_STORE):
        self.store = JsonStore(filename)

    def put(self, key: str, value):
        # simple wrapper for storing single values
        self.store.put(key, value=value)

    def get(self, key: str, default=None):
        if self.store.exists(key):
            try:
                return self.store.get(key)['value']
            except Exception:
                return default
        return default

    # Higher-level helpers
    def set_contact(self, name: str, phone: str):
        self.put('contact_name', name)
        self.put('contact_phone', phone)

    def get_contact(self):
        name = self.get('contact_name', '')
        phone = self.get('contact_phone', '')
        return {"name": name, "phone": phone}
