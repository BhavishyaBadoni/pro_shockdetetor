# app/tts_handler.py
from plyer import tts
from logger import get_logger

logger = get_logger(__name__)

def speak(text: str):
    """
    Speak a text message using plyer tts.
    On desktop, plyer TTS may not be available; handle exceptions gracefully.
    """
    try:
        tts.speak(text)
    except Exception as e:
        # Fallback: just log
        logger.info("TTS fallback: %s", text)
