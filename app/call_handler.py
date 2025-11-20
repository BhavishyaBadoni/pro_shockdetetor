# app/call_handler.py
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from logger import get_logger
from storage import Storage

logger = get_logger(__name__)

# NOTE: Import platform-specific call code lazily (so desktop-run works)
def _make_phone_call(phone_number: str):
    """
    Attempt to make a call.
    On Android the recommended approach is to use android intents via pyjnius.
    We try to use pyjnius if available; otherwise fall back to opening dialer
    (which requires user tap to call).
    """
    try:
        # Android specific
        from jnius import autoclass, cast
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        activity = PythonActivity.mActivity
        intent = Intent(Intent.ACTION_CALL)
        intent.setData(Uri.parse("tel:" + phone_number))
        activity.startActivity(intent)
    except Exception as e:
        # fallback: try ACTION_DIAL (opens dialer with number, user must press call)
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            activity = PythonActivity.mActivity
            intent = Intent(Intent.ACTION_DIAL)
            intent.setData(Uri.parse("tel:" + phone_number))
            activity.startActivity(intent)
        except Exception:
            logger.exception("Failed to place call programmatically: %s", e)
            # last fallback: log only
            logger.info("Would call: %s", phone_number)

def start_countdown_ui(seconds: int):
    """
    Create a popup with countdown and Cancel button.
    If countdown reaches 0, initiate phone call using stored contact.
    """
    storage = Storage()
    contact_phone = storage.get('contact_phone', None)
    contact_name = storage.get('contact_name', 'Emergency Contact')

    if not contact_phone:
        popup = Popup(title="No contact",
                      content=Label(text="No emergency contact set. Please set one in Contact."),
                      size_hint=(0.8, 0.4))
        popup.open()
        return

    box = BoxLayout(orientation='vertical', spacing=10, padding=10)
    label = Label(text=f"Calling {contact_name} in {seconds} seconds", size_hint_y=None, height=40)
    box.add_widget(label)
    btn_layout = BoxLayout(size_hint_y=None, height=48, spacing=8)
    cancel_btn = Button(text="Cancel")
    btn_layout.add_widget(cancel_btn)
    box.add_widget(btn_layout)

    popup = Popup(title="High impact detected", content=box, size_hint=(0.9, 0.5), auto_dismiss=False)

    state = {'remaining': seconds, 'event': None}

    def update(dt):
        state['remaining'] -= 1
        label.text = f"Calling {contact_name} in {state['remaining']} seconds"
        if state['remaining'] <= 0:
            if state['event']:
                state['event'].cancel()
            popup.dismiss()
            logger.info("Countdown finished: calling %s", contact_phone)
            _make_phone_call(contact_phone)

    def on_cancel(instance):
        if state['event']:
            state['event'].cancel()
        popup.dismiss()
        logger.info("Countdown cancelled by user")

    cancel_btn.bind(on_release=on_cancel)
    popup.open()
    # schedule a Clock event every 1 second
    state['event'] = Clock.schedule_interval(update, 1)
