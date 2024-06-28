"""
Self-Reflection Module

This module provides advanced functionality for the AI system to reflect on its own performance,
analyze its capabilities, and suggest potential improvements using advanced analytics.
"""

from typing import List, Dict, Any, Union
from datetime import datetime

from error_handling import log_info, log_error, log_debug, SelfReflectionError
from data_persistence import save_logs, load_logs, save_performance_data, load_performance_data
from advanced_analytics import AdvancedAnalytics
from time_utils import get_timestamp, timestamp_to_datetime


class SelfReflection:
    """Class for managing AI system's self-reflection and performance analysis."""

    def __init__(self, capability_registry: Any, debug_mode: bool = False) -> None:
        """
        Initialize the SelfReflection instance.

        Args:
            capability_registry: The system's capability registry.
            debug_mode: If True, enables verbose debug logging.
        """
        self.capability_registry = capability_registry
        self.debug_mode = debug_mode
        self.advanced_analytics = AdvancedAnalytics(debug_mode)
        self.performance_log = load_logs()
        log_info("SelfReflection instance initialized")
        if self.debug_mode:
            log_debug(f"Loaded {len(self.performance_log)} existing log entries")

    def log_performance(self, task: str, result: Any, execution_time: float,
                        category: str = None) -> None:
        """
        Log the performance of a completed task and save it to persistent storage.

        Args:
            task: The name of the task performed.
            result: The result of the task execution.
            execution_time: The time taken to execute the task, in seconds.
            category: The category of the task.

        Raises:
            SelfReflectionError: If input parameters are invalid.
        """
        try:
            if not isinstance(task, str) or not task.strip():
                raise SelfReflectionError("Task must be a non-empty string")
            if not isinstance(execution_time, (int, float)) or execution_time < 0:
                raise SelfReflectionError("Execution time must be a non-negative number")

            log_entry = {
                "task": task,
                "result": result,
                "execution_time": execution_time,
                "timestamp": get_timestamp(),
                "category": category
            }
            self.performance_log.append(log_entry)
            save_logs([log_entry])
            log_info(f"Performance logged for task: {task}")
            if self.debug_mode:
                log_debug(f"Log entry details: {log_entry}")
        except Exception as e:
            log_error(f"Error logging performance: {str(e)}")
            if self.debug_mode:
                log_debug(f"Detailed error in log_performance: {repr(e)}")
            raise SelfReflectionError(f"Failed to log performance for task '{task}'") from e

    def analyze_performance(self) -> Dict[str, Any]:
        """
        Perform a comprehensive analysis of the system's performance using advanced analytics.

        Returns:
            A dictionary containing various performance metrics and analyses.

        Raises:
            SelfReflectionError: If an error occurs during analysis.
        """
        try:
            all_logs = load_logs()
            if not all_logs:
                log_info("Performance analysis attempted with no data")
                return {"message": "No performance data available."}

            execution_times = [log["execution_time"] for log in all_logs]
            timestamps = [timestamp_to_datetime(log["timestamp"]) for log in all_logs]

            analysis = {
                "timestamp": get_timestamp(),
                "total_tasks": len(all_logs),
                "performance_summary": self.advanced_analytics.performance_summary(execution_times),
                "trend_analysis": self.advanced_analytics.analyze_trend(execution_times),
                "anomalies": self.advanced_analytics.detect_anomalies(execution_times),
                "forecast": self.advanced_analytics.forecast_performance(execution_times),
                "task_categories": self._analyze_task_categories(all_logs),
                "capability_usage": self._analyze_capability_usage(all_logs),
                "areas_for_improvement": self._identify_areas_for_improvement(all_logs)
            }

            log_info("Comprehensive performance analysis completed")
            if self.debug_mode:
                log_debug(f"Analysis results: {analysis}")
            save_performance_data(analysis)
            return analysis
        except Exception as e:
            log_error(f"Error during performance analysis: {str(e)}")
            if self.debug_mode:
                log_debug(f"Detailed error in analyze_performance: {repr(e)}")
            raise SelfReflectionError("Failed to complete performance analysis") from e

    def _analyze_task_categories(self, logs: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Analyze performance by task categories.

        Args:
            logs: List of performance log entries.

        Returns:
            A dictionary of task categories and their performance summaries.
        """
        categories = {}
        for log in logs:
            category = log.get("category", "uncategorized")
            if category not in categories:
                categories[category] = []
            categories[category].append(log["execution_time"])

        category_analysis = {}
        for category, times in categories.items():
            category_analysis[category] = self.advanced_analytics.performance_summary(times)

        if self.debug_mode:
            log_debug(f"Task category analysis completed. Categories analyzed: {len(category_analysis)}")
        return category_analysis

    def _analyze_capability_usage(self, logs: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Analyze the usage and performance of different capabilities.

        Args:
            logs: List of performance log entries.

        Returns:
            A dictionary of capabilities and their usage statistics.
        """
        capabilities = self.capability_registry.list_capabilities()
        capability_usage = {cap: [] for cap in capabilities}

        for log in logs:
            task = log["task"]
            for capability in capabilities:
                if capability in task:
                    capability_usage[capability].append(log["execution_time"])

        capability_analysis = {}
        for cap, times in capability_usage.items():
            if times:
                capability_analysis[cap] = self.advanced_analytics.performance_summary(times)
                capability_analysis[cap]["usage_count"] = len(times)
            else:
                capability_analysis[cap] = {"usage_count": 0}

        if self.debug_mode:
            log_debug(f"Capability usage analysis completed. Capabilities analyzed: {len(capability_analysis)}")
        return capability_analysis

    def _identify_areas_for_improvement(self, logs: List[Dict[str, Any]]) -> List[str]:
        """
        Identify specific areas for improvement based on performance data.

        Args:
            logs: List of performance log entries.

        Returns:
            A list of improvement suggestions.
        """
        improvements = []

        # Analyze slow tasks
        execution_times = [log["execution_time"] for log in logs]
        anomalies = self.advanced_analytics.detect_anomalies(execution_times)
        slow_tasks = [log["task"] for log, is_anomaly in zip(logs, anomalies) if is_anomaly]
        if slow_tasks:
            improvements.append(f"Optimize performance for tasks: {', '.join(set(slow_tasks[:5]))}")

        # Analyze capability reliability
        capability_analysis = self._analyze_capability_usage(logs)
        overall_mean = self.advanced_analytics.performance_summary(execution_times)["mean"]
        low_reliability_caps = [
            cap for cap, analysis in capability_analysis.items()
            if analysis.get("usage_count", 0) > 5 and analysis.get("mean", 0) > 2 * overall_mean
        ]
        if low_reliability_caps:
            improvements.append(f"Improve reliability of capabilities: {', '.join(low_reliability_caps)}")

        # Suggest new capabilities
        all_capabilities = set(self.capability_registry.list_capabilities())
        missing_capabilities = {"natural_language_processing", "image_recognition",
                                "speech_recognition", "machine_learning"} - all_capabilities
        if missing_capabilities:
            improvements.append(f"Consider adding new capabilities: {', '.join(missing_capabilities)}")

        if self.debug_mode:
            log_debug(f"Areas for improvement identified: {len(improvements)}")
        return improvements

    def generate_report(self) -> str:
        """
        Generate a comprehensive performance report.

        Returns:
            A formatted string containing the performance report.

        Raises:
            SelfReflectionError: If an error occurs during report generation.
        """
        try:
            analysis = self.analyze_performance()
            if "message" in analysis:
                return analysis["message"]

            report = [f"Performance Report (as of {analysis['timestamp']}):\n"]
            
            report.append("1. Overall Statistics:")
            summary = analysis['performance_summary']
            report.append(f"   - Total tasks completed: {analysis['total_tasks']}")
            report.append(f"   - Average execution time: {summary['mean']:.2f} seconds")
            report.append(f"   - Median execution time: {summary['median']:.2f} seconds")
            report.append(f"   - Standard deviation: {summary['std_dev']:.2f} seconds")
            report.append(f"   - Min execution time: {summary['min']:.2f} seconds")
            report.append(f"   - Max execution time: {summary['max']:.2f} seconds\n")

            report.append("2. Performance Trend:")
            trend = analysis['trend_analysis']
            report.append(f"   - Trend direction: {trend['trend_direction']}")
            report.append(f"   - Trend strength: {trend['trend_strength']:.2f}")
            report.append(f"   - Slope: {trend['slope']:.4f}\n")

            report.append("3. Anomalies:")
            anomalies = analysis['anomalies']
            anomaly_count = sum(anomalies)
            report.append(f"   - Number of anomalies detected: {anomaly_count}\n")

            report.append("4. Performance Forecast:")
            forecast = analysis['forecast']
            for i, value in enumerate(forecast):
                report.append(f"   - Step {i+1}: {value:.2f} seconds")
            report.append("")

            report.append("5. Task Categories:")
            for category, stats in analysis['task_categories'].items():
                report.append(f"   - {category}: {stats['count']} tasks, Avg time {stats['mean']:.2f}s")
            report.append("")

            report.append("6. Capability Usage:")
            for capability, usage in analysis['capability_usage'].items():
                if usage['usage_count'] > 0:
                    report.append(f"   - {capability}: Used {usage['usage_count']} times, "
                                  f"Avg time {usage['mean']:.2f}s")
            report.append("")

            report.append("7. Areas for Improvement:")
            for improvement in analysis['areas_for_improvement']:
                report.append(f"   - {improvement}")

            if self.debug_mode:
                log_debug("Performance report generated successfully")
            return "\n".join(report)
        except Exception as e:
            log_error(f"Error generating performance report: {str(e)}")
            if self.debug_mode:
                log_debug(f"Detailed error in generate_report: {repr(e)}")
            raise SelfReflectionError("Failed to generate performance report") from e


if __name__ == "__main__":
    # Example usage
    from capability_registry import CapabilityRegistry
    capability_dir = "path/to/capabilities"
    registry = CapabilityRegistry(capability_dir, debug_mode=True)
    self_reflection = SelfReflection(registry, debug_mode=True)
    
    # Log some sample performance data
    self_reflection.log_performance("task1", "success", 1.5, "category1")
    self_reflection.log_performance("task2", "failure", 2.0, "category2")
    self_reflection.log_performance("task3", "success", 1.0, "category1")
    
    # Generate and print a report
    report = self_reflection.generate_report()
    print(report)