import pytest
from datetime import datetime, timedelta
from ai_self_enhancement.src.time_utils import get_timestamp, timestamp_to_datetime, get_time_difference
from ai_self_enhancement.src.error_handling import TimeUtilsError

def test_get_timestamp():
    timestamp = get_timestamp()
    assert isinstance(timestamp, str)
    # Check if the timestamp is in the correct format
    datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

def test_timestamp_to_datetime():
    timestamp = "2023-04-15 10:30:00"
    dt = timestamp_to_datetime(timestamp)
    assert isinstance(dt, datetime)
    assert dt.year == 2023
    assert dt.month == 4
    assert dt.day == 15
    assert dt.hour == 10
    assert dt.minute == 30
    assert dt.second == 0

def test_timestamp_to_datetime_invalid_format():
    with pytest.raises(TimeUtilsError):
        timestamp_to_datetime("2023/04/15 10:30:00")

def test_timestamp_to_datetime_invalid_type():
    with pytest.raises(TimeUtilsError):
        timestamp_to_datetime(123456)

def test_get_time_difference():
    start_time = "2023-04-15 10:00:00"
    end_time = "2023-04-15 11:30:00"
    difference = get_time_difference(start_time, end_time)
    assert difference == 5400  # 1.5 hours in seconds

def test_get_time_difference_negative():
    start_time = "2023-04-15 11:00:00"
    end_time = "2023-04-15 10:00:00"
    difference = get_time_difference(start_time, end_time)
    assert difference == -3600  # -1 hour in seconds

def test_get_time_difference_invalid_format():
    with pytest.raises(TimeUtilsError):
        get_time_difference("2023/04/15 10:00:00", "2023-04-15 11:00:00")

def test_get_time_difference_invalid_type():
    with pytest.raises(TimeUtilsError):
        get_time_difference(123456, "2023-04-15 11:00:00")

@pytest.mark.parametrize("start,end,expected", [
    ("2023-04-15 00:00:00", "2023-04-15 00:00:01", 1),
    ("2023-04-15 00:00:00", "2023-04-15 00:01:00", 60),
    ("2023-04-15 00:00:00", "2023-04-15 01:00:00", 3600),
    ("2023-04-15 00:00:00", "2023-04-16 00:00:00", 86400),
])
def test_get_time_difference_various_durations(start, end, expected):
    assert get_time_difference(start, end) == expected

def test_get_timestamp_consistency():
    timestamp1 = get_timestamp()
    timestamp2 = get_timestamp()
    difference = get_time_difference(timestamp1, timestamp2)
    assert difference >= 0
    assert difference < 1  # Assuming the two calls are less than a second apart