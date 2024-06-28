"""
AI Self-Enhancement System

This module serves as the main entry point for the AI Self-Enhancement system.
It integrates the capability registry and self-reflection components to demonstrate
the system's ability to perform tasks and analyze its own performance.
"""

import os
import sys
import logging
import importlib.util
from capability_registry import CapabilityRegistry
from self_reflection import SelfReflection
from time_utils import get_timestamp, get_time_difference
from error_handling import AISelfEnhancementError
from capability_decorator import load_capability, CapabilityValidationError

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AISelfEnhancementSystem:
    """
    The main class for the AI Self-Enhancement System.

    This class integrates the capability registry and self-reflection modules
    to create a system that can perform tasks and analyze its own performance.
    """

    def __init__(self):
        """Initialize the AI Self-Enhancement System."""
        self.capability_registry = CapabilityRegistry()
        self.self_reflection = SelfReflection(self.capability_registry)

    def run(self):
        """
        Run the AI Self-Enhancement System.

        This method demonstrates the system's capabilities by registering initial
        capabilities, performing sample tasks, and analyzing the system's performance.
        """
        try:
            start_time = get_timestamp()
            logging.info(f"AI Self-Enhancement System Initializing... (Start time: {start_time})")

            # Register initial capabilities
            self.register_initial_capabilities()
            self.load_custom_capabilities()

            while True:
                self.display_menu()
                choice = input("Enter your choice: ")

                if choice == '1':
                    task_name = input("Enter task name: ")
                    input_data = input("Enter input data: ")
                    self.perform_task(task_name, input_data)
                elif choice == '2':
                    self.analyze_performance()
                elif choice == '3':
                    self.suggest_improvements()
                elif choice == '4':
                    break
                else:
                    logging.warning("Invalid choice. Please try again.")

            end_time = get_timestamp()
            total_runtime = get_time_difference(start_time, end_time)
            logging.info(f"Total runtime: {total_runtime:.2f} seconds")

        except AISelfEnhancementError as e:
            logging.error(f"An error occurred: {str(e)}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")

    def register_initial_capabilities(self):
        """Register the initial set of capabilities for the system."""
        self.capability_registry.add_capability(
            "text_analysis",
            "Analyzes text for sentiment and key phrases",
            self.mock_text_analysis
        )
        self.capability_registry.add_capability(
            "data_processing",
            "Processes numerical data",
            self.mock_data_processing
        )

    def load_custom_capabilities(self):
        """Load custom capabilities from the 'capabilities' directory."""
        capabilities_dir = os.path.join(os.path.dirname(__file__), '..', 'capabilities')
        sys.path.append(capabilities_dir)
        for filename in os.listdir(capabilities_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                try:
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(capabilities_dir, filename))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    for item_name in dir(module):
                        item = getattr(module, item_name)
                        if callable(item) and hasattr(item, 'is_capability'):
                            capability = load_capability(item)
                            if capability:
                                self.capability_registry.add_capability(
                                    capability['name'],
                                    capability['description'],
                                    capability['function']
                                )
                                logging.info(f"Loaded custom capability: {capability['name']}")
                            else:
                                logging.warning(f"Failed to load capability: {item_name}")
                except Exception as e:
                    logging.error(f"Error loading custom capability module {module_name}: {str(e)}")

    def perform_task(self, task_name, input_data):
        """
        Perform a task using the registered capabilities.

        Args:
            task_name (str): The name of the task to perform.
            input_data: The input data for the task.
        """
        try:
            capability = self.capability_registry.get_capability(task_name)
            if capability:
                task_start_time = get_timestamp()
                result = capability["function"](input_data)
                task_end_time = get_timestamp()
                execution_time = get_time_difference(task_start_time, task_end_time)
                self.self_reflection.log_performance(task_name, result, execution_time)
                logging.info(f"Task '{task_name}' completed at {task_end_time}. Result: {result}")
            else:
                logging.warning(f"Task '{task_name}' not found in capabilities.")
        except Exception as e:
            logging.error(f"Error performing task '{task_name}': {str(e)}")

    def analyze_performance(self):
        """Analyze and display the system's performance."""
        analysis = self.self_reflection.analyze_performance()
        logging.info("Performance Analysis:")
        for key, value in analysis.items():
            logging.info(f"{key}: {value}")

    def suggest_improvements(self):
        """Generate and display improvement suggestions."""
        suggestions = self.self_reflection.suggest_improvements()
        logging.info("Improvement Suggestions:")
        for suggestion in suggestions:
            logging.info(f"- {suggestion}")

    def display_menu(self):
        """Display the main menu options."""
        print("\nAI Self-Enhancement System Menu:")
        print("1. Perform a task")
        print("2. Analyze performance")
        print("3. Suggest improvements")
        print("4. Exit")

    # Mock functions for demonstration
    def mock_text_analysis(self, text):
        """
        A mock function for text analysis.

        Args:
            text (str): The text to analyze.

        Returns:
            str: A mock analysis result.
        """
        import time
        time.sleep(0.5)  # Simulate processing time
        return f"Analyzed '{text[:20]}...' (length: {len(text)})"

    def mock_data_processing(self, data):
        """
        A mock function for data processing.

        Args:
            data (list): The data to process.

        Returns:
            str: A mock processing result.
        """
        import time
        time.sleep(0.3)  # Simulate processing time
        return f"Processed {len(data)} data points. Sum: {sum(data)}"

if __name__ == "__main__":
    ai_system = AISelfEnhancementSystem()
    ai_system.run()