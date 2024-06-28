import pytest
from datetime import datetime, timedelta
from ai_self_enhancement.src.time_utils import get_timestamp, timestamp_to_datetime, get_time_difference
from ai_self_enhancement.src.error_handling import TimeUtilsError

def test_get_timestamp():
    timestamp = get_timestamp()
    assert isinstance(timestamp, str)
    # Check if the timestamp is in the correct format
    datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

def test_get_timestamp_microsecond_precision():
    timestamp = get_timestamp(microsecond_precision=True)
    assert isinstance(timestamp, str)
    # Check if the timestamp is in the correct format with microseconds
    datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")

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

def test_timestamp_to_datetime_with_microseconds():
    timestamp = "2023-04-15 10:30:00.123456"
    dt = timestamp_to_datetime(timestamp)
    assert isinstance(dt, datetime)
    assert dt.microsecond == 123456

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

def test_extreme_date_ranges():
    far_past = "1000-01-01 00:00:00"
    far_future = "9999-12-31 23:59:59"
    difference = get_time_difference(far_past, far_future)
    assert difference > 0

def test_debug_mode_logging(caplog):
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    get_timestamp(debug_mode=True)
    assert "Generated timestamp" in caplog.text

def test_timezone_handling():
    # This test assumes the time_utils module uses UTC
    # If it doesn't, adjust the test accordingly
    timestamp = get_timestamp()
    dt = timestamp_to_datetime(timestamp)
    assert dt.tzinfo is None or dt.tzinfo.utcoffset(dt) == timedelta(0)

def test_microsecond_precision_difference():
    start = "2023-04-15 10:00:00.000000"
    end = "2023-04-15 10:00:00.000001"
    difference = get_time_difference(start, end)
    assert difference == pytest.approx(0.000001)

if __name__ == "__main__":
    pytest.main([__file__])