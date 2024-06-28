import pytest
import os
from unittest.mock import patch, MagicMock
from ai_self_enhancement.src.capability_registry import CapabilityRegistry
from ai_self_enhancement.src.error_handling import CapabilityError

# Setup a test capability directory
TEST_CAPABILITY_DIR = os.path.join(os.path.dirname(__file__), 'test_capabilities')
os.makedirs(TEST_CAPABILITY_DIR, exist_ok=True)

# Create test capability files
TEST_CAPABILITY_FILE1 = os.path.join(TEST_CAPABILITY_DIR, 'test_capability1.py')
with open(TEST_CAPABILITY_FILE1, 'w') as f:
    f.write('''
def test_function1(x):
    return x * 2

def test_function2(x, y):
    return x + y
''')

TEST_CAPABILITY_FILE2 = os.path.join(TEST_CAPABILITY_DIR, 'test_capability2.py')
with open(TEST_CAPABILITY_FILE2, 'w') as f:
    f.write('''
def another_function(text):
    return text.upper()
''')

@pytest.fixture
def registry():
    return CapabilityRegistry(TEST_CAPABILITY_DIR)

@pytest.fixture
def debug_registry():
    return CapabilityRegistry(TEST_CAPABILITY_DIR, debug_mode=True)

def test_capability_registry_initialization(registry):
    assert isinstance(registry, CapabilityRegistry)
    assert registry.capability_loader is not None

def test_debug_mode(debug_registry):
    with patch('ai_self_enhancement.src.capability_registry.log_debug') as mock_log_debug:
        debug_registry.list_capabilities()
        mock_log_debug.assert_called()

def test_list_capabilities(registry):
    capabilities = registry.list_capabilities()
    assert isinstance(capabilities, dict)
    assert 'test_capability1.test_function1' in capabilities
    assert 'test_capability1.test_function2' in capabilities
    assert 'test_capability2.another_function' in capabilities

def test_add_capability(registry):
    registry.add_capability("new_capability", "Test description")
    capabilities = registry.list_capabilities()
    assert "new_capability" in capabilities
    assert capabilities["new_capability"] == "Test description"

def test_add_duplicate_capability(registry):
    registry.add_capability("unique_capability", "Test description")
    with pytest.raises(CapabilityError):
        registry.add_capability("unique_capability", "Duplicate description")

def test_add_invalid_capability(registry):
    with pytest.raises(CapabilityError):
        registry.add_capability("", "Empty name")

def test_get_capability(registry):
    registry.add_capability("get_test", "Test description")
    capability = registry.get_capability("get_test")
    assert capability["description"] == "Test description"
    assert callable(capability["function"])

def test_get_nonexistent_capability(registry):
    with pytest.raises(CapabilityError):
        registry.get_capability("nonexistent")

def test_remove_capability(registry):
    registry.add_capability("remove_test", "Test description")
    assert registry.remove_capability("remove_test") is True
    with pytest.raises(CapabilityError):
        registry.get_capability("remove_test")

def test_remove_nonexistent_capability(registry):
    assert registry.remove_capability("nonexistent") is False

def test_execute_capability(registry):
    result = registry.execute_capability("test_capability1.test_function1", 5)
    assert result == 10

    result = registry.execute_capability("test_capability1.test_function2", 3, 4)
    assert result == 7

    result = registry.execute_capability("test_capability2.another_function", "hello")
    assert result == "HELLO"

def test_execute_nonexistent_capability(registry):
    with pytest.raises(CapabilityError):
        registry.execute_capability("nonexistent", 5)

def test_load_capabilities_from_multiple_files(registry):
    capabilities = registry.list_capabilities()
    assert len(capabilities) >= 3  # At least 3 functions from 2 files
    assert 'test_capability1.test_function1' in capabilities
    assert 'test_capability1.test_function2' in capabilities
    assert 'test_capability2.another_function' in capabilities

@patch('ai_self_enhancement.src.capability_registry.importlib.util.spec_from_file_location')
def test_load_capabilities_error(mock_spec, registry):
    mock_spec.side_effect = ImportError("Test import error")
    
    # Force a reload of capabilities
    registry.capability_loader.capabilities = {}
    registry.capability_loader.load_capabilities()

    # Check that no capabilities were loaded due to the error
    assert len(registry.list_capabilities()) == 0

# Clean up the test capability files after all tests
def teardown_module(module):
    os.remove(TEST_CAPABILITY_FILE1)
    os.remove(TEST_CAPABILITY_FILE2)
    os.rmdir(TEST_CAPABILITY_DIR)

if __name__ == "__main__":
    pytest.main([__file__])