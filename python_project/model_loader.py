"""
model_loader.py
────────────────
Loads the trained pipeline (preprocessor + model) and its metadata.
Handles the joblib/pickle fallback and raises clear, actionable errors if
artifacts are missing — instead of a raw stack trace at inference time.
"""

import json
import os

import joblib

import config
from utils import setup_logger

logger = setup_logger(__name__)


class ModelLoadError(Exception):
    """Raised when the model artifact or its metadata cannot be loaded."""


def load_metadata() -> dict:
    """Load model_metadata.json, or return safe defaults if it's missing."""
    if not os.path.exists(config.METADATA_PATH):
        logger.warning(
            f"Metadata file not found at {config.METADATA_PATH}. "
            "Falling back to default feature schema in config.py."
        )
        return {
            "model_name": "unknown",
            "numeric_features": config.DEFAULT_NUMERIC_FEATURES,
            "categorical_features": config.DEFAULT_CATEGORICAL_FEATURES,
            "regions": config.DEFAULT_REGIONS,
            "test_r2": None,
            "model_version": "unknown",
        }

    try:
        with open(config.METADATA_PATH, "r") as f:
            metadata = json.load(f)
        logger.info(f"Loaded metadata for model version {metadata.get('model_version')}")
        return metadata
    except (json.JSONDecodeError, OSError) as exc:
        raise ModelLoadError(f"Failed to read metadata file: {exc}") from exc


def load_model():
    """
    Load the trained pipeline. Tries joblib first (preferred — handles
    numpy arrays more efficiently), falls back to pickle if needed.

    Returns:
        A fitted sklearn Pipeline (preprocessor + model).

    Raises:
        ModelLoadError: if no model artifact can be found or loaded.
    """
    if os.path.exists(config.MODEL_PATH):
        try:
            model = joblib.load(config.MODEL_PATH)
            logger.info(f"Model loaded via joblib from {config.MODEL_PATH}")
            return model
        except Exception as exc:
            logger.warning(f"joblib load failed ({exc}); trying pickle fallback.")

    if os.path.exists(config.MODEL_PATH_PICKLE):
        import pickle
        try:
            with open(config.MODEL_PATH_PICKLE, "rb") as f:
                model = pickle.load(f)
            logger.info(f"Model loaded via pickle from {config.MODEL_PATH_PICKLE}")
            return model
        except Exception as exc:
            raise ModelLoadError(f"Failed to load model via pickle: {exc}") from exc

    raise ModelLoadError(
        f"No model artifact found. Expected one of:\n"
        f"  - {config.MODEL_PATH}\n"
        f"  - {config.MODEL_PATH_PICKLE}\n"
        "Run the notebook's MLOps section (Section 11) to train and save a model first."
    )


def get_model_and_metadata():
    """Convenience function: load both the model and its metadata together."""
    metadata = load_metadata()
    model = load_model()
    return model, metadata
