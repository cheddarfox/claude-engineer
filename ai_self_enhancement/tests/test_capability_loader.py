import pytest
import os
from ai_self_enhancement.src.capability_loader import CapabilityLoader
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
def loader():
    return CapabilityLoader(TEST_CAPABILITY_DIR)

def test_capability_loader_initialization(loader):
    assert isinstance(loader, CapabilityLoader)
    assert loader.capability_dir == TEST_CAPABILITY_DIR

def test_load_capabilities(loader):
    loader.load_capabilities()
    assert 'test_capability1.test_function1' in loader.capabilities
    assert 'test_capability1.test_function2' in loader.capabilities
    assert 'test_capability2.another_function' in loader.capabilities

def test_get_capability(loader):
    capability = loader.get_capability('test_capability1.test_function1')
    assert callable(capability)
    assert capability(5) == 10

def test_get_nonexistent_capability(loader):
    with pytest.raises(KeyError):
        loader.get_capability('nonexistent_capability')

def test_execute_capability(loader):
    result = loader.execute_capability('test_capability1.test_function2', 3, 4)
    assert result == 7

    result = loader.execute_capability('test_capability2.another_function', 'hello')
    assert result == 'HELLO'

def test_execute_nonexistent_capability(loader):
    with pytest.raises(KeyError):
        loader.execute_capability('nonexistent_capability', 5)

# Clean up the test capability files after all tests
def teardown_module(module):
    os.remove(TEST_CAPABILITY_FILE1)
    os.remove(TEST_CAPABILITY_FILE2)
    os.rmdir(TEST_CAPABILITY_DIR)