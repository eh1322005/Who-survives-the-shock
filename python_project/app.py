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

# ── Design tokens — geopolitical risk terminal palette ───────────────────
INK = "#0a0e14"
PANEL = "#12171f"
PANEL_RAISED = "#161c25"
LINE = "#232b36"
LINE_STRONG = "#34404e"
TEXT_PRIMARY = "#e8e6e1"
TEXT_SECONDARY = "#8a93a3"
TEXT_MUTED = "#5a6373"
GOLD = "#d4af37"
TEAL = "#5ba3a3"

TIER_COLORS = {
    "🟢 High Resilience": "#5fa86a",
    "🔵 Medium-High": "#5ba3a3",
    "🟡 Medium-Low": "#c9a23f",
    "🔴 Low Resilience": "#a83838",
}

TIER_LABELS = {
    "🟢 High Resilience": "HIGH RESILIENCE",
    "🔵 Medium-High": "MEDIUM-HIGH",
    "🟡 Medium-Low": "MEDIUM-LOW",
    "🔴 Low Resilience": "LOW RESILIENCE",
}


def inject_styles():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

        html, body, [class*="css"] {{
            font-family: 'IBM Plex Sans', sans-serif;
        }}

        .stApp {{
            background-color: {INK};
            color: {TEXT_PRIMARY};
        }}

        section[data-testid="stSidebar"] {{
            background-color: {PANEL};
            border-right: 1px solid {LINE};
        }}

        section[data-testid="stSidebar"] * {{
            color: {TEXT_PRIMARY};
        }}

        /* ── Header masthead ──────────────────────────────────────── */
        .masthead {{
            border-bottom: 1px solid {LINE_STRONG};
            padding: 0 0 20px 0;
            margin-bottom: 8px;
        }}
        .masthead-eyebrow {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 11px;
            letter-spacing: 0.18em;
            color: {TEAL};
            text-transform: uppercase;
            margin: 0 0 6px 0;
        }}
        .masthead-title {{
            font-family: 'IBM Plex Serif', serif;
            font-weight: 600;
            font-size: 34px;
            color: {TEXT_PRIMARY};
            margin: 0;
            letter-spacing: -0.01em;
        }}
        .masthead-sub {{
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 14px;
            color: {TEXT_SECONDARY};
            margin: 8px 0 0 0;
            max-width: 640px;
            line-height: 1.5;
        }}

        /* ── Section labels ───────────────────────────────────────── */
        .section-label {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 11px;
            letter-spacing: 0.14em;
            color: {TEXT_MUTED};
            text-transform: uppercase;
            border-bottom: 1px solid {LINE};
            padding-bottom: 8px;
            margin: 28px 0 18px 0;
            display: flex;
            justify-content: space-between;
        }}
        .section-label span.idx {{
            color: {GOLD};
        }}

        /* ── Sliders ───────────────────────────────────────────────── */
        div[data-testid="stSlider"] label p {{
            font-family: 'IBM Plex Mono', monospace !important;
            font-size: 12px !important;
            color: {TEXT_SECONDARY} !important;
            letter-spacing: 0.02em;
            text-transform: uppercase;
        }}
        div[data-testid="stSlider"] [data-baseweb="slider"] > div > div {{
            background: {LINE_STRONG} !important;
        }}
        div[data-testid="stSlider"] [role="slider"] {{
            background-color: {GOLD} !important;
            border: 2px solid {INK} !important;
        }}
        div[data-testid="stTickBar"] {{ display: none; }}

        /* ── Select box ────────────────────────────────────────────── */
        div[data-testid="stSelectbox"] label p {{
            font-family: 'IBM Plex Mono', monospace !important;
            font-size: 12px !important;
            color: {TEXT_SECONDARY} !important;
            letter-spacing: 0.02em;
            text-transform: uppercase;
        }}
        div[data-testid="stSelectbox"] > div > div {{
            background-color: {PANEL_RAISED} !important;
            border: 1px solid {LINE_STRONG} !important;
            color: {TEXT_PRIMARY} !important;
        }}

        /* ── Buttons ───────────────────────────────────────────────── */
        .stButton > button {{
            background-color: transparent !important;
            border: 1px solid {GOLD} !important;
            color: {GOLD} !important;
            font-family: 'IBM Plex Mono', monospace !important;
            font-size: 13px !important;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            border-radius: 2px !important;
            padding: 12px 0 !important;
            transition: all 0.15s ease;
        }}
        .stButton > button:hover {{
            background-color: {GOLD} !important;
            color: {INK} !important;
        }}

        /* ── Readout panel ─────────────────────────────────────────── */
        .readout {{
            background: {PANEL};
            border: 1px solid {LINE_STRONG};
            border-left: 3px solid var(--readout-accent, {GOLD});
            padding: 28px 32px;
            margin: 8px 0 24px 0;
        }}
        .readout-eyebrow {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 11px;
            letter-spacing: 0.16em;
            color: {TEXT_MUTED};
            text-transform: uppercase;
            margin: 0 0 12px 0;
        }}
        .readout-value-row {{
            display: flex;
            align-items: baseline;
            gap: 18px;
            flex-wrap: wrap;
        }}
        .readout-value {{
            font-family: 'IBM Plex Mono', monospace;
            font-weight: 600;
            font-size: 56px;
            color: var(--readout-accent, {GOLD});
            line-height: 1;
        }}
        .readout-tier {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 13px;
            letter-spacing: 0.1em;
            color: var(--readout-accent, {GOLD});
            border: 1px solid var(--readout-accent, {GOLD});
            padding: 5px 12px;
            text-transform: uppercase;
        }}

        /* ── Stat strip (sidebar model info) ──────────────────────── */
        .stat-row {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid {LINE};
            font-family: 'IBM Plex Mono', monospace;
            font-size: 12px;
        }}
        .stat-row .k {{ color: {TEXT_MUTED}; }}
        .stat-row .v {{ color: {TEXT_PRIMARY}; }}

        .disclaimer {{
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 12px;
            color: {TEXT_MUTED};
            line-height: 1.6;
            margin-top: 20px;
            padding-top: 16px;
            border-top: 1px solid {LINE};
        }}

        div[data-testid="stDataFrame"] {{
            border: 1px solid {LINE};
        }}

        hr {{ border-color: {LINE} !important; }}

        ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
        ::-webkit-scrollbar-track {{ background: {INK}; }}
        ::-webkit-scrollbar-thumb {{ background: {LINE_STRONG}; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource(show_spinner="Loading trained model...")
def load_model_cached():
    """
    Cache the model load across reruns — Streamlit re-executes the script on
    every interaction, and reloading a multi-MB pipeline each time would be
    slow and unnecessary since the artifact doesn't change between clicks.
    """
    return get_model_and_metadata()


def render_header():
    st.markdown(
        f"""
        <div class="masthead">
            <p class="masthead-eyebrow">Risk intelligence &middot; predictive model</p>
            <p class="masthead-title">{config.APP_TITLE}</p>
            <p class="masthead-sub">
                Estimate a country's Composite Resilience Score from its six domain
                scores. Trained on World Bank indicators across 100 countries,
                2000&ndash;2023.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_info(metadata: dict):
    with st.sidebar:
        st.markdown(
            "<p style='font-family:IBM Plex Mono,monospace; font-size:11px; "
            f"letter-spacing:0.14em; color:{TEXT_MUTED}; text-transform:uppercase; "
            "margin-bottom:16px;'>Model record</p>",
            unsafe_allow_html=True,
        )

        r2 = metadata.get("test_r2")
        rows = [
            ("Estimator", metadata.get("model_name", "unknown")),
            ("Test R&sup2;", f"{r2:.3f}" if r2 is not None else "n/a"),
            ("Version", metadata.get("model_version", "unknown")),
        ]
        rows_html = "".join(
            f"<div class='stat-row'><span class='k'>{k}</span><span class='v'>{v}</span></div>"
            for k, v in rows
        )
        st.markdown(rows_html, unsafe_allow_html=True)

        st.markdown(
            "<p class='disclaimer'>This tool is a decision-support aid, not a "
            "substitute for full World Bank data collection. Predictions are "
            "estimates.</p>",
            unsafe_allow_html=True,
        )


def render_inputs(numeric_features: list, valid_regions: list):
    st.markdown(
        "<div class='section-label'><span><span class='idx'>01</span>&nbsp;&nbsp;Domain inputs</span>"
        "<span>Scale 0.00&ndash;1.00</span></div>",
        unsafe_allow_html=True,
    )

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

    st.markdown(
        "<div class='section-label'><span><span class='idx'>02</span>&nbsp;&nbsp;Region</span></div>",
        unsafe_allow_html=True,
    )
    region = st.selectbox(
        "Region", options=valid_regions if valid_regions else ["Unknown"],
        label_visibility="collapsed",
    )

    return domain_scores, region


def render_prediction(prediction: float, tier: str):
    color = TIER_COLORS.get(tier, GOLD)
    tier_label = TIER_LABELS.get(tier, tier)
    st.markdown(
        f"""
        <div class="readout" style="--readout-accent: {color};">
            <p class="readout-eyebrow">Composite resilience score &middot; predicted</p>
            <div class="readout-value-row">
                <span class="readout-value">{prediction:.3f}</span>
                <span class="readout-tier">{tier_label}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_domain_chart(domain_scores: dict):
    categories = list(domain_scores.keys())
    values = list(domain_scores.values())

    fig = go.Figure(go.Bar(
        x=values, y=categories, orientation="h",
        marker_color=GOLD,
        marker_line_width=0,
        text=[f"{v:.2f}" for v in values],
        textposition="outside",
        textfont=dict(family="IBM Plex Mono", color=TEXT_PRIMARY, size=12),
    ))
    fig.update_layout(
        xaxis_range=[0, 1],
        height=320,
        margin=dict(l=10, r=30, t=10, b=10),
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font=dict(family="IBM Plex Sans", color=TEXT_SECONDARY, size=12),
        xaxis=dict(gridcolor=LINE, zerolinecolor=LINE, tickfont=dict(family="IBM Plex Mono")),
        yaxis=dict(gridcolor=LINE, tickfont=dict(family="IBM Plex Mono", size=11)),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def main():
    inject_styles()
    render_header()

    try:
        model, metadata = load_model_cached()
    except ModelLoadError as exc:
        st.error(
            "Could not load the trained model.\n\n"
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

    st.write("")
    predict_clicked = st.button("Run prediction", type="primary", use_container_width=True)

    if predict_clicked:
        try:
            validated = validate_inputs(domain_scores, region, numeric_features, valid_regions)
        except ValueError as exc:
            st.error(f"Invalid input: {exc}")
            logger.warning(f"Validation error: {exc}")
            st.stop()

        input_row = pd.DataFrame([validated])[numeric_features + ["Region"]]

        try:
            prediction = float(model.predict(input_row)[0])
            prediction = min(max(prediction, 0.0), 1.0)
        except Exception as exc:
            st.error("An unexpected error occurred while generating the prediction.")
            logger.exception(f"Prediction failed: {exc}")
            st.stop()

        tier = classify_tier(prediction)
        logger.info(f"Prediction made: score={prediction:.4f}, tier={tier}, region={region}")

        st.markdown(
            "<div class='section-label'><span><span class='idx'>03</span>&nbsp;&nbsp;Result</span></div>",
            unsafe_allow_html=True,
        )
        render_prediction(prediction, tier)

        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.markdown(
                f"<p style='font-family:IBM Plex Mono,monospace; font-size:11px; "
                f"letter-spacing:0.1em; color:{TEXT_MUTED}; text-transform:uppercase; "
                f"margin-bottom:10px;'>Input distribution</p>",
                unsafe_allow_html=True,
            )
            render_domain_chart(domain_scores)
        with col_b:
            st.markdown(
                f"<p style='font-family:IBM Plex Mono,monospace; font-size:11px; "
                f"letter-spacing:0.1em; color:{TEXT_MUTED}; text-transform:uppercase; "
                f"margin-bottom:10px;'>Domain breakdown</p>",
                unsafe_allow_html=True,
            )
            breakdown_df = pd.DataFrame({
                "Domain": list(domain_scores.keys()),
                "Score": [round(v, 3) for v in domain_scores.values()],
            }).sort_values("Score", ascending=False)
            st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
    else:
        st.markdown(
            f"<p style='font-family:IBM Plex Mono,monospace; font-size:12px; "
            f"color:{TEXT_MUTED}; margin-top:8px;'>"
            "Set the domain scores and region above, then run the prediction.</p>",
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
