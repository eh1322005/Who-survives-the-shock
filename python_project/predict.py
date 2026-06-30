"""
predict.py
──────────
Command-line interface for scoring a single country's domain inputs against
the trained Composite Resilience Score model.

Usage:
    python predict.py --digital 0.6 --economic 0.5 --food 0.7 \\
        --healthcare 0.65 --political 0.55 --climate 0.6 \\
        --region "Europe & Central Asia"

Run `python predict.py --help` for the full list of options.
"""

import argparse
import sys

import pandas as pd

from model_loader import get_model_and_metadata, ModelLoadError
from utils import setup_logger, validate_inputs, classify_tier

logger = setup_logger(__name__)


def build_arg_parser(numeric_features: list) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Predict a country's Composite Resilience Score from domain inputs."
    )
    # Map friendly CLI flags to the actual feature column names
    flag_map = {
        "Digital Infrastructure": "--digital",
        "Economic Fragility": "--economic",
        "Food Security": "--food",
        "Healthcare": "--healthcare",
        "Political Stability": "--political",
        "Climate & Energy": "--climate",
    }
    for feature in numeric_features:
        flag = flag_map.get(feature, f"--{feature.lower().replace(' ', '_')}")
        parser.add_argument(
            flag, type=float, required=True,
            help=f"{feature} score (0.0 - 1.0)",
        )
    parser.add_argument(
        "--region", type=str, required=True,
        help="Region name (must match a region seen during training).",
    )
    return parser


def parse_args_to_domain_scores(args, numeric_features: list) -> dict:
    flag_to_feature = {
        "digital": "Digital Infrastructure",
        "economic": "Economic Fragility",
        "food": "Food Security",
        "healthcare": "Healthcare",
        "political": "Political Stability",
        "climate": "Climate & Energy",
    }
    args_dict = vars(args)
    domain_scores = {}
    for feature in numeric_features:
        # Find the matching arg key (either the friendly name or the slug fallback)
        matched = None
        for arg_key, feat_name in flag_to_feature.items():
            if feat_name == feature and arg_key in args_dict:
                matched = args_dict[arg_key]
                break
        if matched is None:
            slug = feature.lower().replace(" ", "_").replace("&", "and")
            matched = args_dict.get(slug)
        domain_scores[feature] = matched
    return domain_scores


def main():
    try:
        model, metadata = get_model_and_metadata()
    except ModelLoadError as exc:
        logger.error(str(exc))
        sys.exit(1)

    numeric_features = metadata.get("numeric_features", [])
    valid_regions = metadata.get("regions", [])

    parser = build_arg_parser(numeric_features)
    args = parser.parse_args()

    domain_scores = parse_args_to_domain_scores(args, numeric_features)

    try:
        validated = validate_inputs(domain_scores, args.region, numeric_features, valid_regions)
    except ValueError as exc:
        logger.error(f"Input validation failed: {exc}")
        sys.exit(1)

    input_row = pd.DataFrame([validated])[numeric_features + ["Region"]]

    try:
        prediction = float(model.predict(input_row)[0])
    except Exception as exc:
        logger.exception(f"Prediction failed: {exc}")
        sys.exit(1)

    tier = classify_tier(prediction)

    print("\n──────────────────────────────────────────")
    print(f"  Predicted Composite Resilience Score: {prediction:.4f}")
    print(f"  Resilience Tier: {tier}")
    print("──────────────────────────────────────────\n")


if __name__ == "__main__":
    main()
