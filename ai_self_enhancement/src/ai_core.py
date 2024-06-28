"""
AI Core Module

This module serves as the main entry point for the AI Self-Enhancement system.
It integrates various components and implements the main decision-making loop.
"""

import os
from capability_registry import CapabilityRegistry
from self_reflection import SelfReflection
from error_handling import log_info, log_error, log_debug, AISelfEnhancementError
from time_utils import get_timestamp, get_time_difference

class AICore:
    def __init__(self, capability_dir: str, debug_mode: bool = False):
        """
        Initialize the AI Core.

        Args:
            capability_dir (str): The directory containing capability modules.
            debug_mode (bool): If True, enables verbose debug logging.
        """
        self.debug_mode = debug_mode
        self.capability_registry = CapabilityRegistry(capability_dir, debug_mode)
        self.self_reflection = SelfReflection(self.capability_registry, debug_mode)
        self.running = False
        self.performance_data = {}
        log_info("AICore initialized")
        if self.debug_mode:
            log_debug("Debug mode enabled")

    def start(self):
        """Start the main AI loop."""
        self.running = True
        log_info("AICore started")
        while self.running:
            try:
                self.execute_task_cycle()
                self.perform_self_reflection()
                self.wait(60)  # Wait for 60 seconds before the next cycle
            except AISelfEnhancementError as e:
                log_error(f"Error in AI core loop: {str(e)}")
                if self.debug_mode:
                    log_debug(f"Detailed error information: {repr(e)}")
                self.running = False
            except Exception as e:
                log_error(f"Unexpected error in AI core loop: {str(e)}")
                if self.debug_mode:
                    log_debug(f"Detailed unexpected error information: {repr(e)}")
                self.running = False

    def stop(self):
        """Stop the main AI loop."""
        self.running = False
        log_info("AICore stopped")

    def wait(self, seconds: int):
        """
        Wait for the specified number of seconds.

        Args:
            seconds (int): The number of seconds to wait.
        """
        if self.debug_mode:
            log_debug(f"Waiting for {seconds} seconds")
        start_time = get_timestamp()
        end_time = get_timestamp()
        while get_time_difference(start_time, end_time) < seconds:
            end_time = get_timestamp()

    def execute_task_cycle(self):
        """Execute a cycle of tasks based on current capabilities."""
        log_info("Executing task cycle")
        capabilities = self.capability_registry.list_capabilities()
        for capability_name, description in capabilities.items():
            try:
                task_result = self.execute_capability(capability_name)
                self.self_reflection.log_performance(capability_name, task_result["result"], task_result["execution_time"], category="capability_execution")
                self.update_performance_data(capability_name, task_result)
            except Exception as e:
                log_error(f"Error executing capability {capability_name}: {str(e)}")
                if self.debug_mode:
                    log_debug(f"Detailed error for capability {capability_name}: {repr(e)}")

    def execute_capability(self, capability_name: str):
        """
        Execute a specific capability and return the result.

        Args:
            capability_name (str): The name of the capability to execute.

        Returns:
            dict: A dictionary containing the result, execution time, and category of the executed capability.
        """
        log_info(f"Executing capability: {capability_name}")
        start_time = get_timestamp()
        
        try:
            result = self.capability_registry.execute_capability(capability_name)
            execution_status = "success"
        except Exception as e:
            log_error(f"Error during capability execution: {str(e)}")
            if self.debug_mode:
                log_debug(f"Detailed capability execution error: {repr(e)}")
            result = None
            execution_status = "failure"
        
        end_time = get_timestamp()
        execution_time = get_time_difference(start_time, end_time)
        
        if self.debug_mode:
            log_debug(f"Capability {capability_name} executed in {execution_time} seconds with status: {execution_status}")
        
        return {
            "result": result,
            "execution_time": execution_time,
            "category": "capability_execution"
        }

    def perform_self_reflection(self):
        """Perform self-reflection and act on the insights."""
        log_info("Performing self-reflection")
        try:
            analysis = self.self_reflection.analyze_performance()
            self.act_on_insights(analysis)
        except Exception as e:
            log_error(f"Error during self-reflection: {str(e)}")
            if self.debug_mode:
                log_debug(f"Detailed self-reflection error: {repr(e)}")

    def act_on_insights(self, analysis):
        """
        Act on the insights generated by self-reflection.

        Args:
            analysis (dict): A dictionary containing the analysis results from self-reflection.
        """
        log_info("Acting on self-reflection insights")
        
        # Handle performance trend
        trend = analysis.get('trend_analysis', {})
        if trend.get('trend_direction') == 'decreasing' and trend.get('trend_strength', 0) > 0.5:
            self.address_decreasing_performance(trend)

        # Handle anomalies
        anomalies = analysis.get('anomalies', [])
        if any(anomalies):
            self.address_anomalies(analysis.get('performance_summary', {}), anomalies)

        # Handle areas for improvement
        for improvement in analysis.get('areas_for_improvement', []):
            try:
                if "Optimize performance for tasks" in improvement:
                    self.optimize_slow_tasks(improvement)
                elif "Improve reliability of capabilities" in improvement:
                    self.improve_capability_reliability(improvement)
                elif "Consider adding new capabilities" in improvement:
                    self.consider_new_capabilities(improvement)
            except Exception as e:
                log_error(f"Error acting on insight: {str(e)}")
                if self.debug_mode:
                    log_debug(f"Detailed insight action error: {repr(e)}")

    def address_decreasing_performance(self, trend):
        """
        Address a decreasing performance trend.

        Args:
            trend (dict): Trend analysis results.
        """
        log_info(f"Addressing decreasing performance trend. Slope: {trend.get('slope', 'N/A')}")
        # Implement logic to address decreasing performance
        # This could involve adjusting resource allocation, triggering system optimizations, etc.

    def address_anomalies(self, performance_summary, anomalies):
        """
        Address detected anomalies in performance.

        Args:
            performance_summary (dict): Summary of performance statistics.
            anomalies (list): List of boolean values indicating anomalies.
        """
        anomaly_count = sum(anomalies)
        log_info(f"Addressing {anomaly_count} detected anomalies")
        # Implement logic to handle anomalies
        # This could involve investigating specific tasks, adjusting thresholds, etc.

    def optimize_slow_tasks(self, improvement):
        """
        Optimize performance for slow tasks.

        Args:
            improvement (str): Description of the improvement to be made.
        """
        log_info(f"Optimizing slow tasks: {improvement}")
        # Implement logic to optimize slow tasks
        # This could involve code refactoring, algorithm improvements, or resource reallocation

    def improve_capability_reliability(self, improvement):
        """
        Improve reliability of underperforming capabilities.

        Args:
            improvement (str): Description of the improvement to be made.
        """
        log_info(f"Improving capability reliability: {improvement}")
        # Implement logic to improve capability reliability
        # This could involve additional training, error handling improvements, or capability redesign

    def consider_new_capabilities(self, improvement):
        """
        Consider adding new capabilities to the system.

        Args:
            improvement (str): Description of the improvement to be made.
        """
        log_info(f"Considering new capabilities: {improvement}")
        # Implement logic to evaluate and potentially add new capabilities
        # This could involve researching new algorithms, integrating new libraries, or expanding the system's functionality

    def update_performance_data(self, capability: str, task_result: dict):
        """
        Update the performance data for a given capability.

        Args:
            capability (str): The name of the capability.
            task_result (dict): The result of the task execution.
        """
        if capability not in self.performance_data:
            self.performance_data[capability] = []
        self.performance_data[capability].append(task_result)
        if self.debug_mode:
            log_debug(f"Updated performance data for {capability}: {task_result}")

if __name__ == "__main__":
    debug_env = os.getenv('AI_DEBUG', 'False').lower() == 'true'
    capability_dir = os.path.join(os.path.dirname(__file__), "capabilities")
    ai_core = AICore(capability_dir, debug_mode=debug_env)
    ai_core.start()