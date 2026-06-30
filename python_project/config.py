"""
config.py
─────────
Centralized configuration for the Global Resilience Score prediction service.

All paths and constants used by model_loader.py, predict.py, utils.py, and
app.py are defined here so there is a single source of truth.
"""

import os

# ── Paths ─────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")

MODEL_PATH = os.path.join(ARTIFACTS_DIR, "resilience_model_latest.joblib")
MODEL_PATH_PICKLE = os.path.join(ARTIFACTS_DIR, "resilience_model_latest.pkl")
METADATA_PATH = os.path.join(ARTIFACTS_DIR, "model_metadata.json")

LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# ── Feature schema (fallback defaults; overridden by model_metadata.json) ──
DEFAULT_NUMERIC_FEATURES = [
    "Digital Infrastructure",
    "Economic Fragility",
    "Food Security",
    "Healthcare",
    "Political Stability",
    "Climate & Energy",
]
DEFAULT_CATEGORICAL_FEATURES = ["Region"]
DEFAULT_REGIONS = [
    "East Asia & Pacific",
    "Europe & Central Asia",
    "Latin America & Caribbean",
    "Middle East & North Africa",
    "North America",
    "South Asia",
    "Sub-Saharan Africa",
]

FEATURE_MIN = 0.0
FEATURE_MAX = 1.0

# ── App settings ─────────────────────────────────────────────────────────
APP_TITLE = "Global Resilience Score Predictor"
APP_ICON = "🌍"

# ── Environment variables (override defaults if set) ────────────────────
# Example: export RESILIENCE_MODEL_PATH=/custom/path/model.joblib
MODEL_PATH = os.environ.get("RESILIENCE_MODEL_PATH", MODEL_PATH)
LOG_LEVEL = os.environ.get("RESILIENCE_LOG_LEVEL", "INFO")
