# app/monitor.py
import threading
import time
import math
from kivy.clock import Clock

from plyer import accelerometer

from tts_handler import speak
from call_handler import start_countdown_ui
from logger import get_logger
from utils import moving_average

logger = get_logger(__name__)

class ShockMonitor:
    def __init__(self, storage, sample_rate=0.05, debounce=3):
        self.storage = storage
        self.sample_rate = sample_rate  # seconds between reads
        self.debounce = debounce
        self._running = False
        self._thread = None
        self._buffer = []
        self._buffer_size = 5  # smoothing window
        self._lock = threading.Lock()

    def start(self):
        try:
            accelerometer.enable()
        except Exception:
            logger.warning("Accelerometer enable failed (desktop or plyer limitation)")
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        try:
            accelerometer.disable()
        except Exception:
            pass

    def _run(self):
        consecutive = 0
        while self._running:
            vals = None
            try:
                vals = accelerometer.acceleration
            except Exception:
                vals = None
            if not vals or vals == (None, None, None):
                # on desktop or if sensor uninitialized, sleep and continue
                time.sleep(self.sample_rate)
                continue

            ax, ay, az = vals
            g = math.sqrt((ax or 0) ** 2 + (ay or 0) ** 2 + (az or 0) ** 2)

            # smoothing
            with self._lock:
                self._buffer.append(g)
                if len(self._buffer) > self._buffer_size:
                    self._buffer.pop(0)
                g_smooth = moving_average(self._buffer)

            threshold = float(self.storage.get('threshold', 30.0))
            if g_smooth >= threshold:
                consecutive += 1
            else:
                consecutive = 0

            if consecutive >= self.debounce:
                # schedule UI alert on main thread
                Clock.schedule_once(lambda dt: self._trigger_alert(g_smooth))
                logger.info("Triggering alert: g=%.2f threshold=%.2f", g_smooth, threshold)
                consecutive = 0

            time.sleep(self.sample_rate)

    def _trigger_alert(self, g_value):
        # speak and show a countdown popup managed by call_handler
        countdown = int(self.storage.get('countdown', 20))
        speak(f"High impact detected. If you are okay press Cancel. Calling emergency contact in {countdown} seconds.")
        start_countdown_ui(countdown)
