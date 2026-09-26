"""
Basic unit tests for the LLMOps pipeline.
Add more comprehensive tests as needed.
"""
import importlib
import sys
from unittest.mock import patch

import pytest
from src.config import Config


def test_config_loaded():
    """Test that configuration values are loaded."""
    assert Config.AZURE_OPENAI_API_KEY is not None
    assert Config.AZURE_OPENAI_ENDPOINT is not None


def test_vector_store_type():
    """Test vector store type configuration."""
    assert Config.VECTOR_STORE_TYPE in ["chroma", "azure_search"]


def test_mlflow_config():
    """Test MLflow configuration."""
    assert Config.MLFLOW_TRACKING_URI is not None
    assert Config.MLFLOW_EXPERIMENT_NAME is not None


def test_monitoring_does_not_configure_mlflow_when_disabled(monkeypatch):
    """MLflow initialization should be skipped when explicitly disabled."""
    monkeypatch.setenv("USE_MLFLOW", "false")
    monkeypatch.setenv("MLFLOW_TRACKING_URI", "http://localhost:5000")

    sys.modules.pop("src.monitoring", None)

    with patch("mlflow.set_tracking_uri") as mock_set_tracking, patch("mlflow.set_experiment") as mock_set_experiment:
        import src.monitoring as monitoring
        importlib.reload(monitoring)

    mock_set_tracking.assert_not_called()
    mock_set_experiment.assert_not_called()
