# app/main.py
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

from storage import Storage
from monitor import ShockMonitor
from logger import get_logger

KV_FILE = "app/ui.kv"

logger = get_logger(__name__)

class HomeScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class ContactScreen(Screen):
    pass

class LogScreen(Screen):
    pass

class Root(ScreenManager):
    pass

class ShockApp(App):
    def build(self):
        Builder.load_file(KV_FILE)
        self.storage = Storage()
        self.monitor = ShockMonitor(storage=self.storage)
        try:
            self.monitor.start()
            logger.info("Shock monitor started")
        except Exception as e:
            logger.exception("Failed to start monitor: %s", e)
        return Root()

    def on_stop(self):
        try:
            self.monitor.stop()
            logger.info("Shock monitor stopped")
        except Exception:
            pass

if __name__ == "__main__":
    ShockApp().run()

