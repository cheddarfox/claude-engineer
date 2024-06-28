"""
Capability Loader Module

This module provides functionality for dynamically loading and managing capability functions
from separate files or modules. It enables the AI system to extend its capabilities
without modifying core components.
"""

import os
import importlib.util
from typing import Dict, Callable, Any
from error_handling import log_info, log_error, log_debug

class CapabilityLoader:
    """
    A class to dynamically load and manage capability functions.
    """

    def __init__(self, capability_dir: str, debug_mode: bool = False):
        """
        Initialize the CapabilityLoader.

        Args:
            capability_dir (str): The directory containing capability modules.
            debug_mode (bool): If True, enables verbose debug logging.
        """
        self.capability_dir = capability_dir
        self.debug_mode = debug_mode
        self.capabilities: Dict[str, Callable] = {}
        self.load_capabilities()

    def load_capabilities(self):
        """
        Scan the capability directory and load all capability functions.
        """
        try:
            for filename in os.listdir(self.capability_dir):
                if filename.endswith(".py") and not filename.startswith("__"):
                    module_name = filename[:-3]  # Remove .py extension
                    module_path = os.path.join(self.capability_dir, filename)
                    self.load_capability_module(module_name, module_path)
            
            log_info(f"Loaded {len(self.capabilities)} capabilities")
            if self.debug_mode:
                log_debug(f"Loaded capabilities: {list(self.capabilities.keys())}")
        except Exception as e:
            log_error(f"Error loading capabilities: {str(e)}")

    def load_capability_module(self, module_name: str, module_path: str):
        """
        Load a single capability module and its functions.

        Args:
            module_name (str): The name of the module to load.
            module_path (str): The file path of the module to load.
        """
        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for item_name in dir(module):
                item = getattr(module, item_name)
                if callable(item) and not item_name.startswith("__"):
                    capability_name = f"{module_name}.{item_name}"
                    self.capabilities[capability_name] = item
            
            if self.debug_mode:
                log_debug(f"Loaded module: {module_name}")
        except Exception as e:
            log_error(f"Error loading module {module_name}: {str(e)}")

    def get_capability(self, capability_name: str) -> Callable:
        """
        Retrieve a capability function by name.

        Args:
            capability_name (str): The name of the capability to retrieve.

        Returns:
            Callable: The capability function.

        Raises:
            KeyError: If the capability is not found.
        """
        if capability_name not in self.capabilities:
            raise KeyError(f"Capability '{capability_name}' not found")
        return self.capabilities[capability_name]

    def execute_capability(self, capability_name: str, *args: Any, **kwargs: Any) -> Any:
        """
        Execute a capability function by name.

        Args:
            capability_name (str): The name of the capability to execute.
            *args: Positional arguments to pass to the capability function.
            **kwargs: Keyword arguments to pass to the capability function.

        Returns:
            Any: The result of the capability function execution.

        Raises:
            KeyError: If the capability is not found.
        """
        try:
            capability = self.get_capability(capability_name)
            result = capability(*args, **kwargs)
            if self.debug_mode:
                log_debug(f"Executed capability: {capability_name}")
            return result
        except Exception as e:
            log_error(f"Error executing capability '{capability_name}': {str(e)}")
            raise

if __name__ == "__main__":
    # Example usage and testing
    capability_dir = os.path.join(os.path.dirname(__file__), "capabilities")
    loader = CapabilityLoader(capability_dir, debug_mode=True)

    # List all loaded capabilities
    print("Loaded capabilities:", list(loader.capabilities.keys()))

    # Execute a capability (assuming a 'test_capability.hello' function exists)
    try:
        result = loader.execute_capability("test_capability.hello", name="AI")
        print("Execution result:", result)
    except KeyError:
        print("Test capability not found. Please ensure a test capability module is present in the capabilities directory.")