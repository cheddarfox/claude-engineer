import pytest
from ai_self_enhancement.src.capability_registry import CapabilityRegistry
from ai_self_enhancement.src.error_handling import CapabilityError

def test_capability_registry_initialization():
    registry = CapabilityRegistry()
    assert len(registry.capabilities) == 0

def test_add_capability():
    registry = CapabilityRegistry()
    registry.add_capability("test_capability", "Test description", lambda x: x)
    assert "test_capability" in registry.capabilities
    assert registry.capabilities["test_capability"]["description"] == "Test description"
    assert callable(registry.capabilities["test_capability"]["function"])

def test_add_duplicate_capability():
    registry = CapabilityRegistry()
    registry.add_capability("test_capability", "Test description", lambda x: x)
    with pytest.raises(CapabilityError):
        registry.add_capability("test_capability", "Duplicate description", lambda x: x)

def test_add_invalid_capability():
    registry = CapabilityRegistry()
    with pytest.raises(CapabilityError):
        registry.add_capability("", "Empty name", lambda x: x)
    with pytest.raises(CapabilityError):
        registry.add_capability("invalid_function", "Invalid function", "not_a_function")

def test_get_capability():
    registry = CapabilityRegistry()
    registry.add_capability("test_capability", "Test description", lambda x: x)
    capability = registry.get_capability("test_capability")
    assert capability["description"] == "Test description"
    assert callable(capability["function"])

def test_get_nonexistent_capability():
    registry = CapabilityRegistry()
    assert registry.get_capability("nonexistent") is None

def test_list_capabilities():
    registry = CapabilityRegistry()
    registry.add_capability("capability1", "Description 1", lambda x: x)
    registry.add_capability("capability2", "Description 2", lambda x: x*2)
    capabilities = registry.list_capabilities()
    assert "capability1" in capabilities
    assert "capability2" in capabilities
    assert len(capabilities) == 2

def test_remove_capability():
    registry = CapabilityRegistry()
    registry.add_capability("test_capability", "Test description", lambda x: x)
    assert registry.remove_capability("test_capability") is True
    assert "test_capability" not in registry.capabilities

def test_remove_nonexistent_capability():
    registry = CapabilityRegistry()
    assert registry.remove_capability("nonexistent") is False

def test_capability_execution():
    registry = CapabilityRegistry()
    registry.add_capability("double", "Doubles the input", lambda x: x * 2)
    capability = registry.get_capability("double")
    assert capability["function"](5) == 10