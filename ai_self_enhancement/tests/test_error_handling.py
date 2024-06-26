import pytest
from ai_self_enhancement.src.error_handling import (
    AISelfEnhancementError,
    CapabilityError,
    SelfReflectionError,
    TimeUtilsError,
    log_info,
    log_warning,
    log_error
)

def test_ai_self_enhancement_error():
    with pytest.raises(AISelfEnhancementError):
        raise AISelfEnhancementError("Test error")

def test_capability_error():
    with pytest.raises(CapabilityError):
        raise CapabilityError("Test capability error")

def test_self_reflection_error():
    with pytest.raises(SelfReflectionError):
        raise SelfReflectionError("Test self-reflection error")

def test_time_utils_error():
    with pytest.raises(TimeUtilsError):
        raise TimeUtilsError("Test time utils error")

def test_logging_functions(caplog):
    log_info("Test info message")
    log_warning("Test warning message")
    log_error("Test error message")

    assert "Test info message" in caplog.text
    assert "Test warning message" in caplog.text
    assert "Test error message" in caplog.text

    assert "INFO" in caplog.text
    assert "WARNING" in caplog.text
    assert "ERROR" in caplog.text