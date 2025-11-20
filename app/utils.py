# app/utils.py
from typing import Iterable
import time
import math

def moving_average(data: Iterable[float]) -> float:
    data = [d for d in data if d is not None]
    if not data:
        return 0.0
    return sum(data) / len(data)

def current_timestamp() -> float:
    return time.time()
