"""
app.py
──────
Streamlit web application for the Global Resilience Score Predictor.

Loads the trained pipeline produced in Section 11 of
Global_Resilience_Final.ipynb, accepts user-provided domain scores via
sliders, validates them, and displays the predicted Composite Resilience
Score with a tier classification and a domain breakdown chart.

Run with:
    streamlit run app.py
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import config
from model_loader import get_model_and_metadata, ModelLoadError
from utils import setup_logger, validate_inputs, classify_tier

logger = setup_logger(__name__)

st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
)

TIER_COLORS = {
    "🟢 High Resilience": "#2ecc71",
    "🔵 Medium-High": "#3498db",
    "🟡 Medium-Low": "#f1c40f",
    "🔴 Low Resilience": "#e74c3c",
}


@st.cache_resource(show_spinner="Loading trained model...")
def load_model_cached():
    """
    Cache the model load across reruns — Streamlit re-executes the script on
    every interaction, and reloading a multi-MB pipeline each time would be
    slow and unnecessary since the artifact doesn't change between clicks.
    """
    return get_model_and_metadata()


def render_header():
    st.title(f"{config.APP_ICON} {config.APP_TITLE}")
    st.caption(
        "Predict a country's Composite Resilience Score from its six domain "
        "scores, using the model trained in the Global Resilience Index project."
    )


def render_sidebar_info(metadata: dict):
    with st.sidebar:
        st.markdown("### Model Information")
        st.write(f"**Model:** {metadata.get('model_name', 'unknown')}")
        r2 = metadata.get("test_r2")
        if r2 is not None:
            st.write(f"**Test R²:** {r2:.3f}")
        st.write(f"**Version:** {metadata.get('model_version', 'unknown')}")
        st.markdown("---")
        st.caption(
            "This tool is a decision-support aid, not a substitute for "
            "full World Bank data collection. Predictions are estimates."
        )


def render_inputs(numeric_features: list, valid_regions: list):
    st.markdown("### Step 1 — Enter Domain Scores")
    st.caption("All scores are on a 0.0 (worst) to 1.0 (best) normalized scale.")

    col1, col2 = st.columns(2)
    half = len(numeric_features) // 2
    left_features = numeric_features[:half]
    right_features = numeric_features[half:]

    domain_scores = {}
    with col1:
        for feature in left_features:
            domain_scores[feature] = st.slider(
                feature, min_value=0.0, max_value=1.0, value=0.5, step=0.01,
                key=f"slider_{feature}",
            )
    with col2:
        for feature in right_features:
            domain_scores[feature] = st.slider(
                feature, min_value=0.0, max_value=1.0, value=0.5, step=0.01,
                key=f"slider_{feature}",
            )

    st.markdown("### Step 2 — Select Region")
    region = st.selectbox("Region", options=valid_regions if valid_regions else ["Unknown"])

    return domain_scores, region


def render_prediction(prediction: float, tier: str):
    color = TIER_COLORS.get(tier, "#888888")
    st.markdown(
        f"""
        <div style="
            background:{color}22; border:2px solid {color}; border-radius:12px;
            padding:24px 32px; margin:16px 0; text-align:center;">
            <h1 style="color:{color}; margin:0; font-size:48px; font-weight:800;">
                {prediction:.3f}
            </h1>
            <p style="margin:8px 0 0 0; font-size:18px;">Predicted Composite Resilience Score</p>
            <p style="margin:4px 0 0 0; font-size:15px; color:{color};"><b>{tier}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_domain_chart(domain_scores: dict):
    categories = list(domain_scores.keys())
    values = list(domain_scores.values())

    fig = go.Figure(go.Bar(
        x=values, y=categories, orientation="h",
        marker_color="#3498db",
        text=[f"{v:.2f}" for v in values],
        textposition="outside",
    ))
    fig.update_layout(
        xaxis_range=[0, 1],
        title="Your Input Domain Scores",
        height=350,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)


def main():
    render_header()

    try:
        model, metadata = load_model_cached()
    except ModelLoadError as exc:
        st.error(
            "❌ Could not load the trained model.\n\n"
            f"**Details:** {exc}\n\n"
            "Make sure you have run Section 11 (MLOps) of "
            "`Global_Resilience_Final.ipynb` to train and save a model, "
            "and that the `artifacts/` folder sits next to this app."
        )
        st.stop()

    numeric_features = metadata.get("numeric_features", config.DEFAULT_NUMERIC_FEATURES)
    valid_regions = metadata.get("regions", config.DEFAULT_REGIONS)

    render_sidebar_info(metadata)

    domain_scores, region = render_inputs(numeric_features, valid_regions)

    st.markdown("---")

    if st.button("🔮 Predict Resilience Score", type="primary", use_container_width=True):
        try:
            validated = validate_inputs(domain_scores, region, numeric_features, valid_regions)
        except ValueError as exc:
            st.error(f"⚠️ Invalid input: {exc}")
            logger.warning(f"Validation error: {exc}")
            st.stop()

        input_row = pd.DataFrame([validated])[numeric_features + ["Region"]]

        try:
            prediction = float(model.predict(input_row)[0])
            prediction = min(max(prediction, 0.0), 1.0)
        except Exception as exc:
            st.error("❌ An unexpected error occurred while generating the prediction.")
            logger.exception(f"Prediction failed: {exc}")
            st.stop()

        tier = classify_tier(prediction)
        logger.info(f"Prediction made: score={prediction:.4f}, tier={tier}, region={region}")

        render_prediction(prediction, tier)

        col_a, col_b = st.columns([1, 1])
        with col_a:
            render_domain_chart(domain_scores)
        with col_b:
            st.markdown("### Domain Breakdown")
            breakdown_df = pd.DataFrame({
                "Domain": list(domain_scores.keys()),
                "Score": [round(v, 3) for v in domain_scores.values()],
            }).sort_values("Score", ascending=False)
            st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
    else:
        st.info("👆 Set the domain scores and region above, then click **Predict Resilience Score**.")


if __name__ == "__main__":
    main()
