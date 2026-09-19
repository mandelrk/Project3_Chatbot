# import time
# from typing import Dict, Any
# import mlflow

# class MetricsCollector:
#     """
#     Collects and logs performance and usage metrics.
#     """
#     def __init__(self):
#         self.metrics = {}

#     def track_latency(self, func):
#         """Decorator to track function latency"""
#         def wrapper(*args, **kwargs):
#             start_time = time.time()
#             result = func(*args, **kwargs)
#             duration = time.time() - start_time
            
#             func_name = func.__name__
#             mlflow.log_metric(f"{func_name}_latency", duration)
#             return result
#         return wrapper

#     def log_token_usage(self, prompt_tokens: int, completion_tokens: int, model: str):
#         """Logs token usage to MLflow"""
#         total_tokens = prompt_tokens + completion_tokens
#         mlflow.log_metric("prompt_tokens", prompt_tokens)
#         mlflow.log_metric("completion_tokens", completion_tokens)
#         mlflow.log_metric("total_tokens", total_tokens)
#         mlflow.log_param("model", model)

#     def log_custom_metric(self, key: str, value: float):
#         mlflow.log_metric(key, value)

import time
from typing import Dict, Any

from src.config import Config

# MLflow is optional — import only if enabled
if Config.USE_MLFLOW:
    import mlflow
else:
    mlflow = None


class MetricsCollector:
    """
    Collects and logs performance and usage metrics.
    MLflow logging is optional and safely skipped when disabled.
    """

    def __init__(self):
        self.metrics = {}

    def _safe_log_metric(self, key: str, value: float):
        """Safely log a metric only if MLflow is enabled."""
        if not Config.USE_MLFLOW or mlflow is None:
            return
        try:
            mlflow.log_metric(key, value)
        except Exception as e:
            print(f"[MLflow metric skipped] {e}")

    def _safe_log_param(self, key: str, value: Any):
        """Safely log a parameter only if MLflow is enabled."""
        if not Config.USE_MLFLOW or mlflow is None:
            return
        try:
            mlflow.log_param(key, value)
        except Exception as e:
            print(f"[MLflow param skipped] {e}")

    def track_latency(self, func):
        """Decorator to track function latency (MLflow optional)."""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start_time

            func_name = func.__name__
            self._safe_log_metric(f"{func_name}_latency", duration)

            return result
        return wrapper

    def log_token_usage(self, prompt_tokens: int, completion_tokens: int, model: str):
        """Logs token usage to MLflow (optional)."""
        total_tokens = prompt_tokens + completion_tokens

        self._safe_log_metric("prompt_tokens", prompt_tokens)
        self._safe_log_metric("completion_tokens", completion_tokens)
        self._safe_log_metric("total_tokens", total_tokens)
        self._safe_log_param("model", model)

    def log_custom_metric(self, key: str, value: float):
        """Logs a custom metric (optional)."""
        self._safe_log_metric(key, value)
