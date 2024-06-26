"""
Capability Registry Module

This module provides a registry for managing AI system capabilities.
It allows for adding, retrieving, listing, and removing capabilities dynamically.
"""

class CapabilityRegistry:
    """
    A class to manage the AI system's capabilities.

    This registry allows for dynamic addition, retrieval, and removal of capabilities,
    enabling the AI system to evolve and adapt its functionalities over time.
    """

    def __init__(self):
        """Initialize an empty capability registry."""
        self.capabilities = {}

    def add_capability(self, name, description, function):
        """
        Add a new capability to the registry.

        Args:
            name (str): The name of the capability.
            description (str): A brief description of what the capability does.
            function (callable): The function that implements the capability.

        Returns:
            None
        """
        self.capabilities[name] = {
            "description": description,
            "function": function
        }

    def get_capability(self, name):
        """
        Retrieve a capability from the registry.

        Args:
            name (str): The name of the capability to retrieve.

        Returns:
            dict or None: A dictionary containing the capability's description and function,
                          or None if the capability is not found.
        """
        return self.capabilities.get(name)

    def list_capabilities(self):
        """
        List all capabilities currently in the registry.

        Returns:
            list: A list of names of all registered capabilities.
        """
        return list(self.capabilities.keys())

    def remove_capability(self, name):
        """
        Remove a capability from the registry.

        Args:
            name (str): The name of the capability to remove.

        Returns:
            bool: True if the capability was successfully removed, False if it wasn't found.
        """
        if name in self.capabilities:
            del self.capabilities[name]
            return True
        return False

# Example usage:
# registry = CapabilityRegistry()
# registry.add_capability("text_analysis", "Analyzes text for sentiment and key phrases", text_analysis_function)
# print(registry.list_capabilities())
# capability = registry.get_capability("text_analysis")
# if capability:
#     result = capability["function"]("Sample text")
#     print(result)