import pytest
from ai_self_enhancement.src.error_handling import (
    AISelfEnhancementError,
    CapabilityError,
    SelfReflectionError,
    TimeUtilsError,
    log_info,
    log_warning,
    log_error,
    log_debug
)

def test_ai_self_enhancement_error():
    with pytest.raises(AISelfEnhancementError) as exc_info:
        raise AISelfEnhancementError("Test error")
    assert str(exc_info.value) == "Test error"
    assert isinstance(exc_info.value, Exception)

def test_capability_error():
    with pytest.raises(CapabilityError) as exc_info:
        raise CapabilityError("Test capability error")
    assert str(exc_info.value) == "Test capability error"
    assert isinstance(exc_info.value, AISelfEnhancementError)

def test_self_reflection_error():
    with pytest.raises(SelfReflectionError) as exc_info:
        raise SelfReflectionError("Test self-reflection error")
    assert str(exc_info.value) == "Test self-reflection error"
    assert isinstance(exc_info.value, AISelfEnhancementError)

def test_time_utils_error():
    with pytest.raises(TimeUtilsError) as exc_info:
        raise TimeUtilsError("Test time utils error")
    assert str(exc_info.value) == "Test time utils error"
    assert isinstance(exc_info.value, AISelfEnhancementError)

def test_logging_functions(caplog):
    log_info("Test info message")
    log_warning("Test warning message")
    log_error("Test error message")
    log_debug("Test debug message")

    assert "Test info message" in caplog.text
    assert "Test warning message" in caplog.text
    assert "Test error message" in caplog.text
    assert "Test debug message" in caplog.text

    assert "INFO" in caplog.text
    assert "WARNING" in caplog.text
    assert "ERROR" in caplog.text
    assert "DEBUG" in caplog.text

def test_debug_mode_logging(caplog):
    import os
    os.environ['AI_DEBUG'] = 'true'
    
    log_debug("Debug mode test message")
    assert "Debug mode test message" in caplog.text
    assert "DEBUG" in caplog.text
    
    os.environ['AI_DEBUG'] = 'false'
    log_debug("This should not appear")
    assert "This should not appear" not in caplog.text

    # Clean up
    del os.environ['AI_DEBUG']

if __name__ == "__main__":
    pytest.main([__file__])