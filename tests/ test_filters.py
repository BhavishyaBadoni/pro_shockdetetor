# tests/test_filters.py
import pytest
from app.utils import moving_average

def test_moving_average_empty():
    assert moving_average([]) == 0.0

def test_moving_average_values():
    arr = [1.0, 2.0, 3.0, 4.0]
    assert moving_average(arr) == pytest.approx(2.5)

def test_moving_average_with_none():
    arr = [1.0, None, 3.0]
    assert moving_average(arr) == pytest.approx(2.0)
