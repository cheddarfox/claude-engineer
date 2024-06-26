"""
Capability Registry Module

This module provides a registry for managing AI system capabilities.
It allows for adding, retrieving, listing, and removing capabilities dynamically.
"""

from error_handling import CapabilityError, log_info, log_error

class CapabilityRegistry:
    """
    A class to manage the AI system's capabilities.

    This registry allows for dynamic addition, retrieval, and removal of capabilities,
    enabling the AI system to evolve and adapt its functionalities over time.
    """

    def __init__(self):
        """Initialize an empty capability registry."""
        self.capabilities = {}
        log_info("Capability Registry initialized")

    def add_capability(self, name, description, function):
        """
        Add a new capability to the registry.

        Args:
            name (str): The name of the capability.
            description (str): A brief description of what the capability does.
            function (callable): The function that implements the capability.

        Returns:
            None

        Raises:
            CapabilityError: If the capability name already exists or if invalid input is provided.
        """
        if not isinstance(name, str) or not name.strip():
            raise CapabilityError("Capability name must be a non-empty string")
        if not isinstance(description, str):
            raise CapabilityError("Capability description must be a string")
        if not callable(function):
            raise CapabilityError("Capability function must be callable")

        if name in self.capabilities:
            raise CapabilityError(f"Capability '{name}' already exists")

        self.capabilities[name] = {
            "description": description,
            "function": function
        }
        log_info(f"Added new capability: {name}")

    def get_capability(self, name):
        """
        Retrieve a capability from the registry.

        Args:
            name (str): The name of the capability to retrieve.

        Returns:
            dict or None: A dictionary containing the capability's description and function,
                          or None if the capability is not found.

        Raises:
            CapabilityError: If the provided name is not a string.
        """
        if not isinstance(name, str):
            raise CapabilityError("Capability name must be a string")

        capability = self.capabilities.get(name)
        if capability is None:
            log_info(f"Attempted to retrieve non-existent capability: {name}")
        return capability

    def list_capabilities(self):
        """
        List all capabilities currently in the registry.

        Returns:
            list: A list of names of all registered capabilities.
        """
        capabilities = list(self.capabilities.keys())
        log_info(f"Listed {len(capabilities)} capabilities")
        return capabilities

    def remove_capability(self, name):
        """
        Remove a capability from the registry.

        Args:
            name (str): The name of the capability to remove.

        Returns:
            bool: True if the capability was successfully removed, False if it wasn't found.

        Raises:
            CapabilityError: If the provided name is not a string.
        """
        if not isinstance(name, str):
            raise CapabilityError("Capability name must be a string")

        if name in self.capabilities:
            del self.capabilities[name]
            log_info(f"Removed capability: {name}")
            return True
        else:
            log_info(f"Attempted to remove non-existent capability: {name}")
            return False

# Example usage:
# try:
#     registry = CapabilityRegistry()
#     registry.add_capability("text_analysis", "Analyzes text for sentiment and key phrases", text_analysis_function)
#     print(registry.list_capabilities())
#     capability = registry.get_capability("text_analysis")
#     if capability:
#         result = capability["function"]("Sample text")
#         print(result)
# except CapabilityError as e:
#     log_error(f"An error occurred in the Capability Registry: {str(e)}")