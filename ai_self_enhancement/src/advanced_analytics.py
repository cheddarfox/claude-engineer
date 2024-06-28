"""
Advanced Analytics Module

This module provides advanced analytical capabilities for the AI self-enhancement system.
It includes methods for trend analysis, anomaly detection, and performance forecasting.
"""

import numpy as np
from scipy import stats
from sklearn.ensemble import IsolationForest
from statsmodels.tsa.arima.model import ARIMA
from typing import List, Dict, Any
from error_handling import log_info, log_error, log_debug

class AdvancedAnalytics:
    def __init__(self, debug_mode: bool = False):
        self.debug_mode = debug_mode
        log_info("AdvancedAnalytics module initialized")
        if self.debug_mode:
            log_debug("Debug mode enabled in AdvancedAnalytics")

    def analyze_trend(self, data: List[float]) -> Dict[str, Any]:
        """
        Perform trend analysis on the given data.

        Args:
            data (List[float]): Time series data for analysis.

        Returns:
            Dict[str, Any]: A dictionary containing trend analysis results.
        """
        try:
            x = np.arange(len(data))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, data)
            
            trend_strength = abs(r_value)
            trend_direction = "increasing" if slope > 0 else "decreasing"
            
            result = {
                "slope": slope,
                "intercept": intercept,
                "r_squared": r_value**2,
                "p_value": p_value,
                "trend_strength": trend_strength,
                "trend_direction": trend_direction
            }
            
            log_info(f"Trend analysis completed. Trend direction: {trend_direction}")
            if self.debug_mode:
                log_debug(f"Trend analysis details: {result}")
            
            return result
        except Exception as e:
            log_error(f"Error in trend analysis: {str(e)}")
            raise

    def detect_anomalies(self, data: List[float], contamination: float = 0.1) -> List[bool]:
        """
        Detect anomalies in the given data using Isolation Forest algorithm.

        Args:
            data (List[float]): Time series data for anomaly detection.
            contamination (float): The proportion of outliers in the data set.

        Returns:
            List[bool]: A list of boolean values indicating whether each data point is an anomaly.
        """
        try:
            clf = IsolationForest(contamination=contamination, random_state=42)
            clf.fit(np.array(data).reshape(-1, 1))
            anomalies = clf.predict(np.array(data).reshape(-1, 1))
            anomalies = [True if a == -1 else False for a in anomalies]
            
            num_anomalies = sum(anomalies)
            log_info(f"Anomaly detection completed. {num_anomalies} anomalies found.")
            if self.debug_mode:
                log_debug(f"Anomaly detection details: {anomalies}")
            
            return anomalies
        except Exception as e:
            log_error(f"Error in anomaly detection: {str(e)}")
            raise

    def forecast_performance(self, data: List[float], steps: int = 5) -> List[float]:
        """
        Forecast future performance based on historical data using ARIMA model.

        Args:
            data (List[float]): Historical time series data for forecasting.
            steps (int): Number of steps to forecast into the future.

        Returns:
            List[float]: Forecasted values for the specified number of steps.
        """
        try:
            model = ARIMA(data, order=(1, 1, 1))
            results = model.fit()
            forecast = results.forecast(steps=steps)
            
            log_info(f"Performance forecast completed for {steps} steps.")
            if self.debug_mode:
                log_debug(f"Forecast details: {forecast.tolist()}")
            
            return forecast.tolist()
        except Exception as e:
            log_error(f"Error in performance forecasting: {str(e)}")
            raise

    def performance_summary(self, data: List[float]) -> Dict[str, float]:
        """
        Generate a summary of performance statistics.

        Args:
            data (List[float]): Performance data to summarize.

        Returns:
            Dict[str, float]: A dictionary containing summary statistics.
        """
        try:
            summary = {
                "mean": np.mean(data),
                "median": np.median(data),
                "std_dev": np.std(data),
                "min": np.min(data),
                "max": np.max(data)
            }
            
            log_info("Performance summary generated.")
            if self.debug_mode:
                log_debug(f"Performance summary details: {summary}")
            
            return summary
        except Exception as e:
            log_error(f"Error in generating performance summary: {str(e)}")
            raise

if __name__ == "__main__":
    # Example usage
    analytics = AdvancedAnalytics(debug_mode=True)
    
    # Sample data
    sample_data = [1.2, 2.3, 3.1, 4.2, 5.5, 3.8, 7.1, 8.2, 9.5, 8.8]
    
    # Trend analysis
    trend_result = analytics.analyze_trend(sample_data)
    print("Trend Analysis Result:", trend_result)
    
    # Anomaly detection
    anomalies = analytics.detect_anomalies(sample_data)
    print("Anomalies:", anomalies)
    
    # Performance forecasting
    forecast = analytics.forecast_performance(sample_data, steps=3)
    print("Forecast:", forecast)
    
    # Performance summary
    summary = analytics.performance_summary(sample_data)
    print("Performance Summary:", summary)