"""
Self-Reflection Module

This module provides advanced functionality for the AI system to reflect on its own performance,
analyze its capabilities, and suggest potential improvements.
"""

from time_utils import get_timestamp, get_time_difference, timestamp_to_datetime
from error_handling import SelfReflectionError, log_info, log_error
from data_persistence import save_logs, load_logs, save_performance_data, load_performance_data
from collections import defaultdict
from datetime import timedelta

class SelfReflection:
    """
    A class to manage the AI system's self-reflection capabilities with advanced analytics.

    This class allows the system to log its performance, analyze its efficiency,
    track trends, and suggest improvements based on its current capabilities and performance data.
    """

    def __init__(self, capability_registry):
        """
        Initialize the SelfReflection instance.

        Args:
            capability_registry (CapabilityRegistry): The system's capability registry.

        Raises:
            SelfReflectionError: If capability_registry is None.
        """
        if capability_registry is None:
            raise SelfReflectionError("Capability registry cannot be None")
        self.capability_registry = capability_registry
        self.performance_log = load_logs()  # Load existing logs
        log_info("SelfReflection instance initialized")

    def log_performance(self, task, result, execution_time, category=None):
        """
        Log the performance of a completed task and save it to persistent storage.

        Args:
            task (str): The name of the task performed.
            result: The result of the task execution.
            execution_time (float): The time taken to execute the task, in seconds.
            category (str, optional): The category of the task.

        Raises:
            SelfReflectionError: If input parameters are invalid.
        """
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
        save_logs([log_entry])  # Save the new log entry
        log_info(f"Performance logged for task: {task}")

    def analyze_performance(self):
        """
        Perform a comprehensive analysis of the system's performance based on all logged data.

        Returns:
            dict: A dictionary containing various performance metrics and analyses.
        """
        all_logs = load_logs()  # Load all logs for analysis
        if not all_logs:
            log_info("Performance analysis attempted with no data")
            return {"message": "No performance data available."}

        analysis = {
            "timestamp": get_timestamp(),
            "total_tasks": len(all_logs),
            "avg_execution_time": sum(log["execution_time"] for log in all_logs) / len(all_logs),
            "success_rate": self._calculate_success_rate(all_logs),
            "performance_trend": self._analyze_performance_trend(all_logs),
            "task_categories": self._analyze_task_categories(all_logs),
            "capability_usage": self._analyze_capability_usage(all_logs),
            "areas_for_improvement": self._identify_areas_for_improvement(all_logs)
        }

        log_info("Comprehensive performance analysis completed")
        self._save_analysis(analysis)
        return analysis

    def _calculate_success_rate(self, logs):
        """Calculate the overall success rate of tasks."""
        successful_tasks = sum(1 for log in logs if log["result"] == "success")
        return successful_tasks / len(logs) if logs else 0

    def _analyze_performance_trend(self, logs):
        """Analyze the performance trend over time."""
        if len(logs) < 2:
            return "Insufficient data for trend analysis"

        sorted_logs = sorted(logs, key=lambda x: timestamp_to_datetime(x["timestamp"]))
        time_periods = self._divide_into_time_periods(sorted_logs)

        trends = []
        for period, period_logs in time_periods.items():
            avg_execution_time = sum(log["execution_time"] for log in period_logs) / len(period_logs)
            success_rate = self._calculate_success_rate(period_logs)
            trends.append({
                "period": period,
                "avg_execution_time": avg_execution_time,
                "success_rate": success_rate
            })

        return trends

    def _divide_into_time_periods(self, sorted_logs):
        """Divide logs into time periods for trend analysis."""
        start_time = timestamp_to_datetime(sorted_logs[0]["timestamp"])
        end_time = timestamp_to_datetime(sorted_logs[-1]["timestamp"])
        total_duration = end_time - start_time

        if total_duration.days > 30:
            period_duration = timedelta(days=7)  # Weekly periods
        elif total_duration.days > 7:
            period_duration = timedelta(days=1)  # Daily periods
        else:
            period_duration = timedelta(hours=1)  # Hourly periods

        time_periods = defaultdict(list)
        for log in sorted_logs:
            log_time = timestamp_to_datetime(log["timestamp"])
            period = ((log_time - start_time) // period_duration) * period_duration + start_time
            time_periods[period].append(log)

        return time_periods

    def _analyze_task_categories(self, logs):
        """Analyze performance by task categories."""
        categories = defaultdict(list)
        for log in logs:
            category = log.get("category", "uncategorized")
            categories[category].append(log)

        category_analysis = {}
        for category, category_logs in categories.items():
            category_analysis[category] = {
                "total_tasks": len(category_logs),
                "avg_execution_time": sum(log["execution_time"] for log in category_logs) / len(category_logs),
                "success_rate": self._calculate_success_rate(category_logs)
            }

        return category_analysis

    def _analyze_capability_usage(self, logs):
        """Analyze the usage and performance of different capabilities."""
        capabilities = self.capability_registry.list_capabilities()
        capability_usage = {cap: {"count": 0, "total_execution_time": 0, "successes": 0} for cap in capabilities}

        for log in logs:
            task = log["task"]
            for capability in capabilities:
                if capability in task:  # Simple check, can be improved with more sophisticated matching
                    capability_usage[capability]["count"] += 1
                    capability_usage[capability]["total_execution_time"] += log["execution_time"]
                    if log["result"] == "success":
                        capability_usage[capability]["successes"] += 1

        for cap, usage in capability_usage.items():
            if usage["count"] > 0:
                usage["avg_execution_time"] = usage["total_execution_time"] / usage["count"]
                usage["success_rate"] = usage["successes"] / usage["count"]
            else:
                usage["avg_execution_time"] = 0
                usage["success_rate"] = 0

        return capability_usage

    def _identify_areas_for_improvement(self, logs):
        """Identify specific areas for improvement based on performance data."""
        improvements = []

        # Identify consistently slow tasks
        avg_execution_time = sum(log["execution_time"] for log in logs) / len(logs)
        slow_tasks = [log for log in logs if log["execution_time"] > avg_execution_time * 1.5]
        if slow_tasks:
            improvements.append(f"Optimize performance for tasks: {', '.join(set(log['task'] for log in slow_tasks[:5]))}")

        # Identify capabilities with low success rates
        capability_usage = self._analyze_capability_usage(logs)
        low_success_capabilities = [cap for cap, usage in capability_usage.items() if usage["success_rate"] < 0.8 and usage["count"] > 5]
        if low_success_capabilities:
            improvements.append(f"Improve reliability of capabilities: {', '.join(low_success_capabilities)}")

        # Suggest new capabilities
        available_capabilities = set(self.capability_registry.list_capabilities())
        missing_capabilities = set(["natural_language_processing", "image_recognition", "speech_recognition", "machine_learning"]) - available_capabilities
        if missing_capabilities:
            improvements.append(f"Consider adding new capabilities: {', '.join(missing_capabilities)}")

        return improvements

    def _save_analysis(self, analysis):
        """Save the performance analysis results."""
        save_performance_data(analysis)
        log_info("Performance analysis saved")

    def generate_report(self):
        """
        Generate a comprehensive performance report.

        Returns:
            str: A formatted string containing the performance report.
        """
        analysis = self.analyze_performance()
        if "message" in analysis:
            return analysis["message"]

        report = f"Performance Report (as of {analysis['timestamp']}):\n\n"
        report += f"1. Overall Statistics:\n"
        report += f"   - Total tasks completed: {analysis['total_tasks']}\n"
        report += f"   - Average execution time: {analysis['avg_execution_time']:.2f} seconds\n"
        report += f"   - Overall success rate: {analysis['success_rate']:.2%}\n\n"

        report += f"2. Performance Trend:\n"
        for trend in analysis['performance_trend']:
            report += f"   - Period {trend['period']}: Avg time {trend['avg_execution_time']:.2f}s, Success rate {trend['success_rate']:.2%}\n"
        report += "\n"

        report += f"3. Task Categories:\n"
        for category, stats in analysis['task_categories'].items():
            report += f"   - {category}: {stats['total_tasks']} tasks, Avg time {stats['avg_execution_time']:.2f}s, Success rate {stats['success_rate']:.2%}\n"
        report += "\n"

        report += f"4. Capability Usage:\n"
        for capability, usage in analysis['capability_usage'].items():
            report += f"   - {capability}: Used {usage['count']} times, Avg time {usage['avg_execution_time']:.2f}s, Success rate {usage['success_rate']:.2%}\n"
        report += "\n"

        report += f"5. Areas for Improvement:\n"
        for improvement in analysis['areas_for_improvement']:
            report += f"   - {improvement}\n"

        return report

# Example usage:
# try:
#     registry = CapabilityRegistry()
#     self_reflection = SelfReflection(registry)
#     self_reflection.log_performance("text_analysis", "success", 0.5, "nlp")
#     print(self_reflection.generate_report())
# except SelfReflectionError as e:
#     log_error(f"An error occurred in the Self-Reflection module: {str(e)}")