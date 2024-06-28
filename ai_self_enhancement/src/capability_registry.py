"""
Capability Registry Module

This module provides a registry for managing AI system capabilities.
It allows for adding, retrieving, listing, and removing capabilities dynamically.
"""

import os
from typing import Dict, Any, Callable, Optional

from error_handling import CapabilityError, log_info, log_error, log_debug
from data_persistence import save_performance_data, load_performance_data
from capability_loader import CapabilityLoader


class CapabilityRegistry:
    """
    A class to manage the AI system's capabilities.

    This registry allows for dynamic addition, retrieval, and removal of capabilities,
    enabling the AI system to evolve and adapt its functionalities over time.
    """

    def __init__(self, capability_dir: str, debug_mode: bool = False) -> None:
        """
        Initialize the capability registry and load existing capabilities.

        Args:
            capability_dir: The directory containing capability modules.
            debug_mode: If True, enables verbose debug logging.
        """
        self.debug_mode = debug_mode
        self.capability_loader = CapabilityLoader(capability_dir, debug_mode)
        self.capabilities: Dict[str, Dict[str, Any]] = {}
        self._load_capabilities()
        log_info("Capability Registry initialized")
        if self.debug_mode:
            log_debug(f"Loaded {len(self.capabilities)} capabilities")

    def _load_capabilities(self) -> None:
        """Load capabilities from persistent storage and capability loader."""
        stored_data = load_performance_data()
        for entry in stored_data:
            if entry.get("type") == "capability":
                name = entry["name"]
                self.capabilities[name] = {
                    "description": entry["description"],
                    "function": self.capability_loader.get_capability(name)
                }
        if self.debug_mode:
            log_debug(f"Loaded {len(self.capabilities)} capabilities from storage")

    def _save_capabilities(self) -> None:
        """Save capabilities to persistent storage."""
        data_to_save = [
            {
                "type": "capability",
                "name": name,
                "description": info["description"]
            }
            for name, info in self.capabilities.items()
        ]
        save_performance_data(data_to_save)
        if self.debug_mode:
            log_debug(f"Saved {len(data_to_save)} capabilities to storage")

    def add_capability(self, name: str, description: str) -> None:
        """
        Add a new capability to the registry.

        Args:
            name: The name of the capability.
            description: A brief description of what the capability does.

        Raises:
            CapabilityError: If the capability name already exists or if invalid input is provided.
        """
        try:
            if not isinstance(name, str) or not name.strip():
                raise CapabilityError("Capability name must be a non-empty string")
            if not isinstance(description, str):
                raise CapabilityError("Capability description must be a string")

            if name in self.capabilities:
                raise CapabilityError(f"Capability '{name}' already exists")

            function = self.capability_loader.get_capability(name)
            if not function:
                raise CapabilityError(
                    f"Capability function '{name}' not found in loader")

            self.capabilities[name] = {
                "description": description,
                "function": function
            }
            self._save_capabilities()
            log_info(f"Added new capability: {name}")
            if self.debug_mode:
                log_debug(f"Capability details - Name: {name}, Description: {description}")
        except Exception as e:
            log_error(f"Error adding capability '{name}': {str(e)}")
            raise CapabilityError(f"Failed to add capability '{name}'") from e

    def get_capability(self, name: str) -> Dict[str, Any]:
        """
        Retrieve a capability from the registry.

        Args:
            name: The name of the capability to retrieve.

        Returns:
            A dictionary containing the capability's description and function.

        Raises:
            CapabilityError: If the capability is not found or if the provided name is not a string.
        """
        try:
            if not isinstance(name, str):
                raise CapabilityError("Capability name must be a string")

            capability = self.capabilities.get(name)
            if capability is None:
                raise CapabilityError(f"Capability '{name}' not found")

            if self.debug_mode:
                log_debug(f"Retrieved capability: {name}")
            return capability
        except Exception as e:
            log_error(f"Error retrieving capability '{name}': {str(e)}")
            raise CapabilityError(f"Failed to retrieve capability '{name}'") from e

    def list_capabilities(self) -> Dict[str, str]:
        """
        List all capabilities currently in the registry.

        Returns:
            A dictionary of capability names and their descriptions.
        """
        capability_list = {name: info["description"] 
                           for name, info in self.capabilities.items()}
        log_info(f"Listed {len(capability_list)} capabilities")
        if self.debug_mode:
            log_debug(f"Capability list: {list(capability_list.keys())}")
        return capability_list

    def remove_capability(self, name: str) -> bool:
        """
        Remove a capability from the registry.

        Args:
            name: The name of the capability to remove.

        Returns:
            True if the capability was successfully removed, False if it wasn't found.

        Raises:
            CapabilityError: If the provided name is not a string.
        """
        try:
            if not isinstance(name, str):
                raise CapabilityError("Capability name must be a string")

            if name in self.capabilities:
                del self.capabilities[name]
                self._save_capabilities()
                log_info(f"Removed capability: {name}")
                if self.debug_mode:
                    log_debug(f"Capability '{name}' removed from registry")
                return True
            else:
                log_info(f"Attempted to remove non-existent capability: {name}")
                return False
        except Exception as e:
            log_error(f"Error removing capability '{name}': {str(e)}")
            raise CapabilityError(f"Failed to remove capability '{name}'") from e

    def execute_capability(self, name: str, *args: Any, **kwargs: Any) -> Any:
        """
        Execute a capability function by name.

        Args:
            name: The name of the capability to execute.
            *args: Positional arguments to pass to the capability function.
            **kwargs: Keyword arguments to pass to the capability function.

        Returns:
            The result of the capability function execution.

        Raises:
            CapabilityError: If the capability is not found or execution fails.
        """
        try:
            capability = self.get_capability(name)
            result = capability["function"](*args, **kwargs)
            if self.debug_mode:
                log_debug(f"Executed capability: {name}")
            return result
        except Exception as e:
            log_error(f"Error executing capability '{name}': {str(e)}")
            raise CapabilityError(f"Failed to execute capability '{name}'") from e


if __name__ == "__main__":
    # Example usage and testing
    capability_dir = os.path.join(os.path.dirname(__file__), "capabilities")
    registry = CapabilityRegistry(capability_dir, debug_mode=True)
    
    # List all capabilities
    print("Available capabilities:", registry.list_capabilities())
    
    # Add a new capability
    try:
        registry.add_capability("basic_capabilities.greet", "A simple greeting function")
        print("Added new capability")
    except CapabilityError as e:
        print(f"Error adding capability: {e}")
    
    # Execute a capability
    try:
        result = registry.execute_capability("basic_capabilities.greet", name="AI")
        print("Execution result:", result)
    except CapabilityError as e:
        print(f"Error executing capability: {e}")

    # Remove a capability
    removed = registry.remove_capability("basic_capabilities.greet")
    print("Capability removed:", removed)

    # List capabilities again
    print("Updated capabilities:", registry.list_capabilities())