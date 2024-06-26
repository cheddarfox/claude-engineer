"""
AI Self-Enhancement System

This module serves as the main entry point for the AI Self-Enhancement system.
It integrates the capability registry and self-reflection components to demonstrate
the system's ability to perform tasks and analyze its own performance.
"""

from capability_registry import CapabilityRegistry
from self_reflection import SelfReflection
from time_utils import get_timestamp, get_time_difference

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
        start_time = get_timestamp()
        print(f"AI Self-Enhancement System Initializing... (Start time: {start_time})")

        # Register initial capabilities
        self.register_initial_capabilities()

        # Simulate some tasks
        self.perform_task("text_analysis", "This is a sample text for analysis.")
        self.perform_task("data_processing", [1, 2, 3, 4, 5])

        # Analyze performance and suggest improvements
        print("\nPerformance Analysis:")
        print(self.self_reflection.analyze_performance())

        print("\nImprovement Suggestions:")
        for suggestion in self.self_reflection.suggest_improvements():
            print(f"- {suggestion}")

        end_time = get_timestamp()
        total_runtime = get_time_difference(start_time, end_time)
        print(f"\nTotal runtime: {total_runtime:.2f} seconds")

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

    def perform_task(self, task_name, input_data):
        """
        Perform a task using the registered capabilities.

        Args:
            task_name (str): The name of the task to perform.
            input_data: The input data for the task.
        """
        capability = self.capability_registry.get_capability(task_name)
        if capability:
            task_start_time = get_timestamp()
            result = capability["function"](input_data)
            task_end_time = get_timestamp()
            execution_time = get_time_difference(task_start_time, task_end_time)
            self.self_reflection.log_performance(task_name, result, execution_time)
            print(f"Task '{task_name}' completed at {task_end_time}. Result: {result}")
        else:
            print(f"Task '{task_name}' not found in capabilities.")

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