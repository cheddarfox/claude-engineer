"""
Visualization Module

This module provides functions for generating visualizations of project management performance data.
It uses matplotlib to create various charts and graphs that offer insights into task completion,
time management, overall project progress, and token usage.
"""

import matplotlib.pyplot as plt
from typing import List, Dict, Any
import numpy as np
from datetime import datetime

def plot_task_completion_rate(completed_tasks: int, total_tasks: int):
    """
    Generate a pie chart showing the proportion of completed tasks to total tasks.

    Args:
    completed_tasks (int): Number of completed tasks
    total_tasks (int): Total number of tasks

    Returns:
    None (displays the plot)
    """
    labels = 'Completed', 'Remaining'
    sizes = [completed_tasks, total_tasks - completed_tasks]
    colors = ['#ff9999', '#66b3ff']

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Task Completion Rate')
    plt.show()

def plot_task_priority_distribution(priority_counts: Dict[str, int]):
    """
    Generate a bar chart showing the distribution of tasks across different priority levels.

    Args:
    priority_counts (Dict[str, int]): A dictionary with priority levels as keys and task counts as values

    Returns:
    None (displays the plot)
    """
    priorities = list(priority_counts.keys())
    counts = list(priority_counts.values())

    plt.figure(figsize=(8, 6))
    plt.bar(priorities, counts)
    plt.xlabel('Priority Level')
    plt.ylabel('Number of Tasks')
    plt.title('Task Priority Distribution')
    plt.show()

def plot_time_management(planned_times: List[float], actual_times: List[float], task_names: List[str]):
    """
    Generate a grouped bar chart comparing planned vs actual time spent on tasks.

    Args:
    planned_times (List[float]): List of planned times for tasks
    actual_times (List[float]): List of actual times spent on tasks
    task_names (List[str]): List of task names

    Returns:
    None (displays the plot)
    """
    x = np.arange(len(task_names))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))
    rects1 = ax.bar(x - width/2, planned_times, width, label='Planned')
    rects2 = ax.bar(x + width/2, actual_times, width, label='Actual')

    ax.set_ylabel('Time (hours)')
    ax.set_title('Planned vs Actual Time Spent on Tasks')
    ax.set_xticks(x)
    ax.set_xticklabels(task_names, rotation=45, ha='right')
    ax.legend()

    fig.tight_layout()
    plt.show()

def plot_progress_over_time(timestamps: List[str], values: List[float], title: str, y_label: str):
    """
    Generate a line chart showing progress or metric changes over time.

    Args:
    timestamps (List[str]): List of timestamps
    values (List[float]): List of values corresponding to the timestamps
    title (str): Title of the plot
    y_label (str): Label for the y-axis

    Returns:
    None (displays the plot)
    """
    dates = [datetime.fromisoformat(ts) for ts in timestamps]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, values, marker='o')
    plt.xlabel('Date')
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Test the visualization functions
    plot_task_completion_rate(75, 100)
    
    priority_counts = {'High': 10, 'Medium': 15, 'Low': 5}
    plot_task_priority_distribution(priority_counts)
    
    planned_times = [10, 15, 8, 12]
    actual_times = [12, 14, 10, 11]
    task_names = ['Task A', 'Task B', 'Task C', 'Task D']
    plot_time_management(planned_times, actual_times, task_names)
    
    # Test progress over time plot
    timestamps = [
        '2023-03-01T10:00:00',
        '2023-03-15T14:30:00',
        '2023-04-01T09:15:00',
        '2023-04-15T16:45:00',
        '2023-05-01T11:30:00'
    ]
    progress_values = [10, 30, 50, 75, 90]
    plot_progress_over_time(timestamps, progress_values, 'Project Progress Over Time', 'Progress (%)')

    # Test token usage over time plot
    token_usage = [100, 250, 400, 600, 800]
    plot_progress_over_time(timestamps, token_usage, 'Token Usage Over Time', 'Tokens Used')