"""
utils.py
────────
Shared utility functions: logging setup, input validation, and small
reusable helpers used across predict.py, model_loader.py, and app.py.
"""

import logging
import os
import sys

import config


def setup_logger(name: str = "resilience_app") -> logging.Logger:
    """
    Create (or fetch) a configured logger that writes to both console
    and a rotating log file under logs/.
    """
    os.makedirs(config.LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    if logger.handlers:
        # Logger already configured (avoids duplicate handlers on reruns,
        # which matters in Streamlit since scripts re-execute on each interaction)
        return logger

    logger.setLevel(getattr(logging, config.LOG_LEVEL, logging.INFO))

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    try:
        file_handler = logging.FileHandler(config.LOG_FILE)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except OSError:
        # If the filesystem is read-only (some deployment targets), fall back
        # to console-only logging rather than crashing the app.
        logger.warning("Could not create log file; continuing with console logging only.")

    return logger


def validate_domain_score(value, field_name: str) -> float:
    """
    Validate that a single domain score is numeric and within [0, 1].

    Raises:
        ValueError: if the value is missing, non-numeric, or out of range.
    """
    if value is None:
        raise ValueError(f"'{field_name}' is required.")

    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"'{field_name}' must be a number, got: {value!r}")

    if not (config.FEATURE_MIN <= value <= config.FEATURE_MAX):
        raise ValueError(
            f"'{field_name}' must be between {config.FEATURE_MIN} and "
            f"{config.FEATURE_MAX}, got: {value}"
        )

    return value


def validate_inputs(domain_scores: dict, region: str, numeric_features: list, valid_regions: list) -> dict:
    """
    Validate a full set of user inputs before passing them to the model.

    Args:
        domain_scores: dict mapping domain name -> raw user input value.
        region: selected region string.
        numeric_features: list of expected domain feature names.
        valid_regions: list of regions the model was trained on.

    Returns:
        dict of validated, type-cast values ready for the model.

    Raises:
        ValueError: with a clear, user-facing message on the first invalid field.
    """
    validated = {}

    missing = [f for f in numeric_features if f not in domain_scores]
    if missing:
        raise ValueError(f"Missing required domain scores: {missing}")

    for feature in numeric_features:
        validated[feature] = validate_domain_score(domain_scores[feature], feature)

    if not region or not isinstance(region, str):
        raise ValueError("A valid region must be selected.")

    if valid_regions and region not in valid_regions:
        raise ValueError(
            f"Region '{region}' was not seen during training. "
            f"Valid options: {valid_regions}"
        )

    validated["Region"] = region
    return validated


def classify_tier(score: float) -> str:
    """Map a composite score to the same resilience tier labels used in the dashboard."""
    if score >= 0.70:
        return "🟢 High Resilience"
    elif score >= 0.55:
        return "🔵 Medium-High"
    elif score >= 0.40:
        return "🟡 Medium-Low"
    return "🔴 Low Resilience"
