"""
Future Shock Index — Global Resilience Dashboard
Single-file Streamlit application (app.py)
Run: streamlit run app.py
"""

import os, base64
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import pearsonr

# ─────────────────────────────────────────────────────────────────────────────
# 0. PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Future Shock Index · Global Resilience Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# 1. CONSTANTS — derived from ACTUAL data, not assumed
# ─────────────────────────────────────────────────────────────────────────────

# TRUE domains as they exist in the CSVs
DOMAINS = [
    "Climate & Energy",
    "Digital Infrastructure",
    "Economic Fragility",
    "Food Security",
    "Healthcare",
    "Political Stability",
]

# TRUE regions as they exist in the CSVs
REGIONS = [
    "Africa", "Central America & Caribbean", "Central Asia", "East Asia",
    "Europe", "Middle East", "North America", "Oceania",
    "South America", "South Asia", "Other",
]

DOMAIN_ICONS = {
    "Climate & Energy":        "🌡️",
    "Digital Infrastructure":  "💻",
    "Economic Fragility":      "💰",
    "Food Security":           "🌾",
    "Healthcare":              "🏥",
    "Political Stability":     "🏛️",
}

DOMAIN_COLORS = {
    "Climate & Energy":        "#34D399",
    "Digital Infrastructure":  "#38BDF8",
    "Economic Fragility":      "#FBBF24",
    "Food Security":           "#FB923C",
    "Healthcare":              "#818CF8",
    "Political Stability":     "#F472B6",
}

REGION_COLORS = {
    "Europe":                      "#818CF8",
    "East Asia":                   "#38BDF8",
    "Africa":                      "#FBBF24",
    "Middle East":                 "#F87171",
    "South America":               "#34D399",
    "South Asia":                  "#FB923C",
    "North America":               "#A78BFA",
    "Central America & Caribbean": "#F472B6",
    "Central Asia":                "#94A3B8",
    "Oceania":                     "#22D3EE",
    "Other":                       "#64748B",
}

C = {
    "bg":         "#0F1623",
    "surface":    "#192133",
    "surface2":   "#1E2A40",
    "accent":     "#38BDF8",
    "accent2":    "#818CF8",
    "border":     "#263354",
    "text":       "#E2E8F0",
    "muted":      "#94A3B8",
    "success":    "#34D399",
    "warning":    "#FBBF24",
    "danger":     "#F87171",
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "forecast_outputs")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# ─────────────────────────────────────────────────────────────────────────────
# 2. CSS INJECTION (once, here)
# ─────────────────────────────────────────────────────────────────────────────

def _get_logo_b64():
    p = os.path.join(ASSETS_DIR, "logo.png")
    if os.path.exists(p):
        with open(p, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def inject_global_css():
    logo_b64 = _get_logo_b64()
    logo_tag = ""
    if logo_b64:
        logo_tag = f'<img src="data:image/png;base64,{logo_b64}" style="height:30px;width:30px;object-fit:contain;flex-shrink:0;" />'

    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">',
        unsafe_allow_html=True,
    )

    st.markdown(f"""
<style>
/* ── Reset ── */
#MainMenu,footer,header{{visibility:hidden;}}
.block-container{{padding:0 0.6rem !important;max-width:100% !important;}}
html,body,[data-testid="stAppViewContainer"]{{background:#0F1623 !important;color:#E2E8F0;font-family:'Inter',sans-serif;}}
[data-testid="stAppViewContainer"]>.main{{background:#0F1623;}}
section[data-testid="stSidebar"]{{display:none;}}

/* ── Logo header ── */
.fsi-header{{
  display:flex;align-items:center;gap:10px;
  background:#192133;border-bottom:1px solid #263354;
  padding:5px 14px;height:48px;
}}
.fsi-title{{font-size:12px;font-weight:700;color:#E2E8F0;letter-spacing:0.02em;line-height:1.2;margin-bottom:3px;}}
.fsi-sub{{font-size:6px;color:#94A3B8;letter-spacing:0.06em;text-transform:uppercase;line-height:1.2;}}

/* ── Tab bar ── */
.stTabs [data-baseweb="tab-list"]{{
  gap:0;background:#192133;border-bottom:1px solid #263354;padding:0 10px;
}}
.stTabs [data-baseweb="tab"]{{
  height:38px;padding:0 16px;
  font-family:'Inter',sans-serif;font-size:12px;font-weight:500;
  color:#94A3B8;border-bottom:2px solid transparent;background:transparent;
  white-space:nowrap;
}}
.stTabs [aria-selected="true"]{{color:#38BDF8 !important;border-bottom:2px solid #38BDF8 !important;background:transparent !important;}}
.stTabs [data-baseweb="tab-highlight"]{{background:transparent !important;}}
.stTabs [data-baseweb="tab-panel"]{{padding:0 !important;background:#0F1623;}}

/* ── Widgets ── */
.stSelectbox>div>div{{background:#192133 !important;border:1px solid #263354 !important;color:#E2E8F0 !important;font-size:11px !important;}}
.stSlider>div>div>div{{background:#38BDF8 !important;}}
label[data-testid="stWidgetLabel"]{{font-size:10px !important;color:#94A3B8 !important;font-weight:500 !important;margin-bottom:1px !important;}}

/* ── Plotly ── */
.js-plotly-plot .plotly,.js-plotly-plot,.plot-container{{background:rgba(0,0,0,0) !important;}}

/* ── Scrollbar ── */
::-webkit-scrollbar{{width:3px;height:3px;}}
::-webkit-scrollbar-track{{background:#0F1623;}}
::-webkit-scrollbar-thumb{{background:#263354;border-radius:2px;}}

/* ── Layout gaps ── */
[data-testid="stHorizontalBlock"]{{gap:0.5rem !important;}}
[data-testid="stVerticalBlock"]{{gap:0.15rem !important;}}
[data-testid="stVerticalBlockBorderWrapper"]{{overflow:hidden;}}

/* ── Remove extra streamlit padding ── */
div[data-testid="stVerticalBlock"]>div{{padding-top:0 !important;}}
</style>
""", unsafe_allow_html=True)

    # Logo header above tabs
    st.markdown(f"""
<div class="fsi-header">
  {logo_tag}
  <div>
    <div class="fsi-title">Future Shock Index</div>
    <div class="fsi-sub">Global Resilience Dashboard</div>
  </div>
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 3. DATA LOADING & PREPROCESSING
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_data():
    actual    = pd.read_csv(os.path.join(DATA_DIR, "domain_scores_2000_2023.csv"))
    estimated = pd.read_csv(os.path.join(DATA_DIR, "out_of_filter_scores.csv"))
    ranking   = pd.read_csv(os.path.join(DATA_DIR, "global_2030_ranking.csv"))
    forecast  = pd.read_csv(os.path.join(DATA_DIR, "forecast_2030_scenarios.csv"))
    reg_params = pd.read_csv(os.path.join(DATA_DIR, "regression_params.csv"))
    backtest  = pd.read_csv(os.path.join(DATA_DIR, "backtest_results.csv"))

    # --- Composite scores ---
    grp_cols = ["Country Code", "Country Name", "Region", "Year"]
    actual_comp = (actual.groupby(grp_cols)["Domain_Score"]
                   .mean().reset_index()
                   .rename(columns={"Domain_Score": "Composite_Score"}))
    est_comp = (estimated.groupby(grp_cols)["Domain_Score"]
                .mean().reset_index()
                .rename(columns={"Domain_Score": "Composite_Score"}))

    # --- Latest year (2023) ---
    latest_yr = int(actual_comp["Year"].max())
    latest = actual_comp[actual_comp["Year"] == latest_yr].copy()
    latest["Rank"] = latest["Composite_Score"].rank(ascending=False, method="min").astype(int)
    latest["Tier"] = latest["Composite_Score"].apply(assign_tier)
    latest["Risk"] = latest["Composite_Score"].apply(assign_risk)

    est_latest_yr = int(est_comp["Year"].max())
    est_latest = est_comp[est_comp["Year"] == est_latest_yr].copy()
    est_latest["Tier"] = est_latest["Composite_Score"].apply(assign_tier)
    est_latest["Risk"] = est_latest["Composite_Score"].apply(assign_risk)

    # --- Regional / global trends ---
    regional_trend = (actual_comp.groupby(["Region", "Year"])["Composite_Score"]
                      .mean().reset_index())
    global_trend   = (actual_comp.groupby("Year")["Composite_Score"]
                      .mean().reset_index())

    # --- Domain averages per region (latest year) ---
    act_latest_dom = actual[actual["Year"] == latest_yr]
    domain_region  = (act_latest_dom.groupby(["Region", "Domain"])["Domain_Score"]
                      .mean().reset_index())

    # --- Domain change 2000→latest ---
    d_base = actual[actual["Year"] == int(actual["Year"].min())]
    d_end  = actual[actual["Year"] == latest_yr]
    d_base_avg = d_base.groupby("Domain")["Domain_Score"].mean()
    d_end_avg  = d_end.groupby("Domain")["Domain_Score"].mean()
    domain_change = pd.DataFrame({
        "Domain":  d_end_avg.index,
        "Score_End":  d_end_avg.values,
        "Score_Start": d_base_avg.reindex(d_end_avg.index).values,
    })
    domain_change["Change"] = domain_change["Score_End"] - domain_change["Score_Start"]

    # --- P4 change df ---
    base_yr_data = (actual_comp[actual_comp["Year"] == int(actual_comp["Year"].min())]
                    [["Country Code", "Composite_Score"]]
                    .rename(columns={"Composite_Score": "Score_2000"}))
    end_yr_data  = (actual_comp[actual_comp["Year"] == latest_yr]
                    [["Country Code", "Composite_Score", "Country Name", "Region"]]
                    .rename(columns={"Composite_Score": "Score_2023"}))
    change_df = end_yr_data.merge(base_yr_data, on="Country Code", how="inner")
    change_df["Score_Change"] = change_df["Score_2023"] - change_df["Score_2000"]
    change_df["Tier"] = change_df["Score_2023"].apply(assign_tier)
    change_df["Risk"] = change_df["Score_2023"].apply(assign_risk)

    # --- Domain-wide correlation (all years) ---
    domain_wide = actual.pivot_table(
        index=["Country Code", "Year"], columns="Domain", values="Domain_Score"
    )
    corr_matrix = domain_wide.corr()

    return {
        "actual":         actual,
        "estimated":      estimated,
        "ranking":        ranking,
        "forecast":       forecast,
        "reg_params":     reg_params,
        "backtest":       backtest,
        "actual_comp":    actual_comp,
        "est_comp":       est_comp,
        "latest":         latest,
        "est_latest":     est_latest,
        "regional_trend": regional_trend,
        "global_trend":   global_trend,
        "domain_region":  domain_region,
        "domain_change":  domain_change,
        "change_df":      change_df,
        "corr_matrix":    corr_matrix,
        "latest_yr":      latest_yr,
        "base_yr":        int(actual_comp["Year"].min()),
        "years":          sorted(actual_comp["Year"].unique().tolist()),
    }


# ─────────────────────────────────────────────────────────────────────────────
# 4. HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def assign_tier(score):
    if pd.isna(score): return "D"
    if score >= 0.75: return "A"
    if score >= 0.60: return "B"
    if score >= 0.45: return "C"
    return "D"

def assign_risk(score):
    if pd.isna(score): return "Critical"
    if score >= 0.70: return "Low"
    if score >= 0.55: return "Medium"
    if score >= 0.40: return "High"
    return "Critical"

def tier_color(tier):
    return {"A": "#34D399", "B": "#38BDF8", "C": "#FBBF24", "D": "#F87171"}.get(tier, "#94A3B8")

def risk_color(risk):
    return {"Low": "#34D399", "Medium": "#FBBF24", "High": "#F87171", "Critical": "#DC2626"}.get(risk, "#94A3B8")

def conf_color(c):
    return {"High": "#34D399", "Medium": "#FBBF24", "Low": "#F87171"}.get(c, "#94A3B8")

ISO3_TO_ISO2 = {
    "AFG":"AF","ALB":"AL","DZA":"DZ","AGO":"AO","ARG":"AR","ARM":"AM","AUS":"AU","AUT":"AT",
    "AZE":"AZ","BHR":"BH","BGD":"BD","BLR":"BY","BEL":"BE","BLZ":"BZ","BEN":"BJ","BTN":"BT",
    "BOL":"BO","BIH":"BA","BWA":"BW","BRA":"BR","BRN":"BN","BGR":"BG","BFA":"BF","BDI":"BI",
    "CPV":"CV","KHM":"KH","CMR":"CM","CAN":"CA","CAF":"CF","TCD":"TD","CHL":"CL","CHN":"CN",
    "COL":"CO","COD":"CD","COG":"CG","CRI":"CR","CIV":"CI","HRV":"HR","CUB":"CU","CYP":"CY",
    "CZE":"CZ","DNK":"DK","DJI":"DJ","DOM":"DO","ECU":"EC","EGY":"EG","SLV":"SV","ERI":"ER",
    "EST":"EE","SWZ":"SZ","ETH":"ET","FJI":"FJ","FIN":"FI","FRA":"FR","GAB":"GA","GMB":"GM",
    "GEO":"GE","DEU":"DE","GHA":"GH","GIB":"GI","GRC":"GR","GTM":"GT","GIN":"GN","GNB":"GW",
    "GUY":"GY","HTI":"HT","HND":"HN","HUN":"HU","ISL":"IS","IND":"IN","IDN":"ID","IRN":"IR",
    "IRQ":"IQ","IRL":"IE","ISR":"IL","ITA":"IT","JAM":"JM","JPN":"JP","JOR":"JO","KAZ":"KZ",
    "KEN":"KE","PRK":"KP","KOR":"KR","KWT":"KW","KGZ":"KG","LAO":"LA","LVA":"LV","LBN":"LB",
    "LSO":"LS","LBR":"LR","LBY":"LY","LTU":"LT","LUX":"LU","MDG":"MG","MWI":"MW","MYS":"MY",
    "MDV":"MV","MLI":"ML","MLT":"MT","MRT":"MR","MUS":"MU","MEX":"MX","MDA":"MD","MNG":"MN",
    "MNE":"ME","MAR":"MA","MOZ":"MZ","MMR":"MM","NAM":"NA","NPL":"NP","NLD":"NL","NZL":"NZ",
    "NIC":"NI","NER":"NE","NGA":"NG","MKD":"MK","NOR":"NO","OMN":"OM","PAK":"PK","PAN":"PA",
    "PNG":"PG","PRY":"PY","PER":"PE","PHL":"PH","POL":"PL","PRT":"PT","QAT":"QA","ROU":"RO",
    "RUS":"RU","RWA":"RW","SAU":"SA","SEN":"SN","SRB":"RS","SLE":"SL","SGP":"SG","SVK":"SK",
    "SVN":"SI","SOM":"SO","ZAF":"ZA","SSD":"SS","ESP":"ES","LKA":"LK","SDN":"SD","SUR":"SR",
    "SWE":"SE","CHE":"CH","SYR":"SY","TWN":"TW","TJK":"TJ","TZA":"TZ","THA":"TH","TGO":"TG",
    "TTO":"TT","TUN":"TN","TUR":"TR","TKM":"TM","UGA":"UG","UKR":"UA","ARE":"AE","GBR":"GB",
    "USA":"US","URY":"UY","UZB":"UZ","VEN":"VE","VNM":"VN","YEM":"YE","ZMB":"ZM","ZWE":"ZW",
    "HKG":"HK","MAC":"MO","XKX":"XK","PSE":"PS","ABW":"AW","GRL":"GL","AND":"AD","LIE":"LI",
    "MCO":"MC","SMR":"SM","GNQ":"GQ","CYM":"KY","GUM":"GU","ASM":"AS","NCL":"NC","PYF":"PF",
}

def get_flag(code3):
    if not isinstance(code3, str): return "🏳️"
    iso2 = ISO3_TO_ISO2.get(code3.upper())
    if iso2 and len(iso2) == 2:
        try:
            return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in iso2.upper())
        except Exception:
            pass
    return "🏳️"

def pbr(score, color="#38BDF8", h=3):
    """Progress bar HTML"""
    pct = min(max(float(score) * 100, 0), 100)
    return (f'<div style="background:#263354;border-radius:2px;height:{h}px;width:100%;margin-top:3px;">'
            f'<div style="background:{color};border-radius:2px;height:{h}px;width:{pct:.1f}%;"></div></div>')

def badge(text, color="#38BDF8"):
    bg = color + "22"
    border = color + "44"
    return (f'<span style="background:{bg};color:{color};border:1px solid {border};'
            f'border-radius:4px;padding:2px 7px;font-size:9px;font-weight:600;'
            f'font-family:Inter,sans-serif;white-space:nowrap;">{text}</span>')

def base_layout(extra=None):
    """Return base Plotly layout dict — each chart merges this with its own keys"""
    d = {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {
            "family": "Inter,sans-serif",
            "color": "#E2E8F0",
            "size": 11,
        },
    }

    if extra:
        d.update(extra)

    return d
def styled_axis(d=None):
    a = {"gridcolor":"#263354","linecolor":"#263354","tickfont":{"size":9,"color":"#94A3B8"}}
    if d: a.update(d)
    return a

def kpi(label, value, sub="", color="#38BDF8", h=62):
    return f"""
<div style="background:#192133;border:1px solid #263354;border-radius:6px;
            padding:7px 11px;height:{h}px;overflow:hidden;">
  <div style="font-size:11px;color:#94A3B8;font-weight:700;letter-spacing:0.08em;
              text-transform:uppercase;margin-bottom:2px;">{label}</div>

  <div style="font-size:18px;font-weight:700;color:#E2E8F0;
              font-family:'JetBrains Mono',monospace;line-height:1.1;">{value}</div>

  <div style="font-size:10px;color:{color};white-space:nowrap;overflow:hidden;
              text-overflow:ellipsis;">{sub}</div>
</div>"""
# ─────────────────────────────────────────────────────────────────────────────
# 5. PAGE 1 — GLOBAL OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────

def page_global_overview(D):
    # Page-level spacing fix: trim the default bottom padding so there's no
    # dead space at the bottom of the page (top spacing is now handled by
    # the explicit spacer div right before the filter row below).
    st.markdown("""
    <style>
    .block-container {
        padding-bottom: 1.25rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    actual_comp = D["actual_comp"]
    actual      = D["actual"]

    # Spacer to push the filter row down, away from the navbar
    st.markdown('<div style="margin-top: 25px;"></div>', unsafe_allow_html=True)

    # Row 0: filters inline — compact single row
    c0 = st.columns([5, 2, 1])
    with c0[0]:
        sel_year = st.slider("Year", int(D["base_yr"]), int(D["latest_yr"]),
                             int(D["latest_yr"]), key="p1_year",
                             label_visibility="collapsed")
    with c0[1]:
        reg_opts = ["All Regions"] + sorted(actual_comp["Region"].dropna().unique().tolist())
        sel_reg  = st.selectbox("Region", reg_opts, key="p1_reg", label_visibility="collapsed")
    with c0[2]:
        st.markdown(f'<div style="padding-top:6px;font-size:9px;color:#94A3B8;font-weight:600;text-transform:uppercase;">YEAR</div>'
                    f'<div style="font-size:14px;font-weight:700;color:#38BDF8;font-family:\'JetBrains Mono\',monospace;">{sel_year}</div>',
                    unsafe_allow_html=True)

    # Filter
    year_df = actual_comp[actual_comp["Year"] == sel_year].copy()
    year_df["Rank"] = year_df["Composite_Score"].rank(ascending=False, method="min").astype(int)
    year_df["Tier"] = year_df["Composite_Score"].apply(assign_tier)
    year_df["Risk"] = year_df["Composite_Score"].apply(assign_risk)

    fdf = year_df if sel_reg == "All Regions" else year_df[year_df["Region"] == sel_reg]

    # Row 1: KPIs
    kc = st.columns(6)
    if not fdf.empty:
        top   = fdf.nlargest(1, "Composite_Score").iloc[0]
        bot   = fdf.nsmallest(1, "Composite_Score").iloc[0]
        avg   = fdf["Composite_Score"].mean()
        treg  = (fdf.groupby("Region")["Composite_Score"].mean().idxmax()
                 if sel_reg == "All Regions" and fdf["Region"].nunique() > 0 else sel_reg)
        vals = [
            kpi("Countries", str(len(fdf)), f"{sel_year} snapshot"),
            kpi("Global Avg", f"{avg:.3f}", "Mean composite"),
            kpi("Top Region", f'<span title="{treg}" style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:block;">{treg}</span>', "Highest avg score"),
            kpi("Most Resilient", f'{get_flag(top["Country Code"])} <span title="{top["Country Name"]}" style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{top["Country Name"]}</span>',
                f"{top['Composite_Score']:.3f}", "#34D399"),
            kpi("Least Resilient", f'{get_flag(bot["Country Code"])} <span title="{bot["Country Name"]}" style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{bot["Country Name"]}</span>',
                f"{bot['Composite_Score']:.3f}", "#F87171"),
            kpi("Score Range", f"{fdf['Composite_Score'].min():.2f}–{fdf['Composite_Score'].max():.2f}",
                f"Spread {fdf['Composite_Score'].max()-fdf['Composite_Score'].min():.3f}"),
        ]
    else:
        vals = [kpi("No Data","—","No data")] * 6

    for i, col in enumerate(kc):
        col.markdown(vals[i], unsafe_allow_html=True)

    # Row 2: Map | Bar | Strip  — taller charts to fill screen
    mc, bc, sc = st.columns([5, 3.5, 2.5])

    # World Map — taller
    with mc:
        if not fdf.empty:
            fig = px.choropleth(
                fdf,
                locations="Country Code", locationmode="ISO-3",
                color="Composite_Score",
                color_continuous_scale=[[0,"#F87171"],[0.4,"#FBBF24"],[0.7,"#38BDF8"],[1,"#34D399"]],
                range_color=[0, 1],
                hover_name="Country Name",
                hover_data={"Composite_Score":":.3f","Rank":True,"Tier":True,"Region":True},
            )
            fig.update_geos(
                bgcolor="rgba(0,0,0,0)", landcolor="#192133",
                oceancolor="#0F1623", showocean=True,
                lakecolor="#0F1623", showlakes=True,
                framecolor="#263354", showframe=True,
                projection_type="natural earth",
            )
            fig.update_layout(
                **base_layout(),
                height=390,
                margin=dict(t=60, b=0, l=0, r=0),
                title=dict(text="🌍 Global Resilience Map", font=dict(size=11, color="#94A3B8"), x=0.01),
                coloraxis_colorbar=dict(
                    thickness=10, len=0.7,
                    tickfont=dict(size=8, color="#94A3B8"),
                    title=dict(text="Score", font=dict(size=9, color="#94A3B8")),
                ),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown('<div style="height:390px;display:flex;align-items:center;justify-content:center;'
                        'color:#94A3B8;background:#192133;border-radius:6px;">No data</div>', unsafe_allow_html=True)

    # Regional bar — taller
    with bc:
        ra = year_df.groupby("Region")["Composite_Score"].mean().reset_index().sort_values("Composite_Score")
        if not ra.empty:
            fig2 = go.Figure(go.Bar(
                x=ra["Composite_Score"], y=ra["Region"], orientation="h",
                marker_color=[REGION_COLORS.get(r,"#94A3B8") for r in ra["Region"]],
                text=ra["Composite_Score"].map("{:.3f}".format),
                textposition="outside",
                textfont=dict(size=9, color="#94A3B8", family="JetBrains Mono"),
                marker_line_width=0,
            ))
            fig2.update_layout(
    **base_layout(),
    height=390,
    margin=dict(t=60, b=16, l=4, r=52),
    title=dict(
        text="Regional Averages",
        font=dict(size=11, color="#94A3B8"),
        x=0.01
    ),
    xaxis=styled_axis({
        "range": [0, 1.18],
        "dtick": 0.25,
    }),
    yaxis=styled_axis({
        "tickfont": {
            "size": 9,
            "color": "#E2E8F0"
        }
    }),
    bargap=0.25,
)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    # Strip plot — taller
    with sc:
        if not fdf.empty:
            rng = np.random.default_rng(42)
            fig3 = go.Figure()
            for tier, tc in [("A","#34D399"),("B","#38BDF8"),("C","#FBBF24"),("D","#F87171")]:
                td = fdf[fdf["Tier"]==tier]
                if not td.empty:
                    jitter = rng.uniform(-0.42, 0.42, len(td))
                    fig3.add_trace(go.Scatter(
                        x=jitter, y=td["Composite_Score"],
                        mode="markers", name=f"Tier {tier}",
                        marker=dict(color=tc, size=4, opacity=0.80),
                        hovertemplate="<b>%{customdata}</b><br>%{y:.3f}<extra></extra>",
                        customdata=td["Country Name"].values,
                    ))
            for thresh, tc in [(0.75,"#34D399"),(0.60,"#38BDF8"),(0.45,"#FBBF24")]:
                fig3.add_hline(y=thresh, line=dict(color=tc, dash="dot", width=1), opacity=0.4)
            fig3.update_layout(
                **base_layout(),
                height=390,
                margin=dict(t=55, b=16, l=36, r=8),
                title=dict(text="Score Distribution", font=dict(size=11, color="#94A3B8"), x=0.01),
                xaxis=dict(visible=False, range=[-1,1]),
                yaxis=dict(range=[0,1.05], **styled_axis(), dtick=0.2,
                           title=dict(text="Score", font=dict(size=9, color="#94A3B8"))),
                legend=dict(orientation="v", x=0.02, y=0.98,
                            bgcolor="rgba(25,33,51,0.85)", font=dict(size=9, color="#94A3B8")),
            )
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    # Row 3: Executive Summary + Global Trend + Tier Distribution
    if not fdf.empty:
        tier_counts = fdf["Tier"].value_counts().reindex(["A","B","C","D"], fill_value=0)

    sum_col, trend_col, tier_col = st.columns([4, 4, 2])

    if not fdf.empty:
        top  = fdf.nlargest(1,"Composite_Score").iloc[0]
        bot  = fdf.nsmallest(1,"Composite_Score").iloc[0]
        avg  = fdf["Composite_Score"].mean()
        n    = len(fdf)
        treg = fdf.groupby("Region")["Composite_Score"].mean().idxmax() if fdf["Region"].nunique()>0 else "N/A"
        note = f" ({sel_reg})" if sel_reg != "All Regions" else ""
        txt  = (f'In <b>{sel_year}</b>{note}, the Index covers <b>{n} countries</b> with global avg '
                f'<b style="color:#38BDF8;font-family:\'JetBrains Mono\',monospace;">{avg:.3f}</b>. '
                f'<b>{top["Country Name"]}</b> leads '
                f'(<b style="color:#34D399;font-family:\'JetBrains Mono\',monospace;">{top["Composite_Score"]:.3f}</b>), '
                f'while <b>{bot["Country Name"]}</b> remains most fragile '
                f'(<b style="color:#F87171;font-family:\'JetBrains Mono\',monospace;">{bot["Composite_Score"]:.3f}</b>). '
                f'<b>{treg}</b> is the most resilient region on average.')
    else:
        txt = "No data available for the selected filters."
        tier_counts = pd.Series({"A":0,"B":0,"C":0,"D":0})

    with sum_col:
        st.markdown(f"""
<div style="background:#192133;border:1px solid #263354;border-left:3px solid #38BDF8;
            border-radius:6px;padding:10px 14px;margin-top:2px;min-height:120px;">
  <div style="font-size:12px;color:#94A3B8;font-weight:600;letter-spacing:0.1em;
              text-transform:uppercase;margin-bottom:4px;">📋 EXECUTIVE SUMMARY</div>
  <div style="font-size:15px;color:#E2E8F0;line-height:1.5;">{txt}</div>
</div>""", unsafe_allow_html=True)

    with trend_col:
        g_trend = D["global_trend"].sort_values("Year")
        fig_gt = go.Figure()
        fig_gt.add_trace(go.Scatter(
            x=g_trend["Year"], y=g_trend["Composite_Score"],
            mode="lines+markers",
            fill="tozeroy", fillcolor="rgba(56,189,248,0.08)",
            line=dict(color="#38BDF8", width=2),
            marker=dict(size=3, color="#38BDF8"),
            hovertemplate="<b>%{x}</b>: %{y:.3f}<extra></extra>",
        ))
        sel_gt = g_trend[g_trend["Year"] == sel_year]
        if not sel_gt.empty:
            fig_gt.add_trace(go.Scatter(
                x=sel_gt["Year"], y=sel_gt["Composite_Score"],
                mode="markers",
                marker=dict(size=8, color="#FBBF24", symbol="circle",
                            line=dict(width=2, color="#FBBF24")),
                showlegend=False,
                hovertemplate=f"<b>{sel_year}</b>: %{{y:.3f}}<extra>Selected</extra>",
            ))
        y_lo = max(g_trend["Composite_Score"].min() - 0.02, 0)
        y_hi = g_trend["Composite_Score"].max() + 0.02
        fig_gt.update_layout(
            **base_layout(),
            height=140,
            margin=dict(t=24, b=20, l=36, r=10),
            title=dict(text="📈 Global Resilience Trend", font=dict(size=10, color="#94A3B8"), x=0.01),
            xaxis=styled_axis({"dtick": 5}),
            yaxis=styled_axis({"range": [y_lo, y_hi], "dtick": 0.02}),
            showlegend=False,
        )
        st.plotly_chart(fig_gt, use_container_width=True, config={"displayModeBar": False})

    with tier_col:
        fig_tier = go.Figure(go.Bar(
            x=["A","B","C","D"],
            y=[int(tier_counts.get(t,0)) for t in ["A","B","C","D"]],
            marker_color=["#34D399", "#38BDF8", "#FBBF24", "#F87171"],
            text=[int(tier_counts.get(t,0)) for t in ["A","B","C","D"]],
            textposition="outside",
            textfont=dict(size=10, color="#E2E8F0", family="JetBrains Mono"),
            marker_line_width=0,
        ))
        fig_tier.update_layout(
            **base_layout(),
            height=140,
            margin=dict(t=24, b=8, l=8, r=8),
            title=dict(text="Tier Dist.", font=dict(size=10, color="#94A3B8"), x=0.01),
            xaxis=styled_axis({"tickfont": {"size": 10, "color": "#94A3B8"}}),
            yaxis=styled_axis({"visible": False}),
            bargap=0.35,
            showlegend=False,
        )
        st.plotly_chart(fig_tier, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────────────────────────────────────────
# 6. PAGE 2 — DOMAIN INTELLIGENCE
# ─────────────────────────────────────────────────────────────────────────────

def page_domain_intelligence(D):
    # Same page-level spacing fix as the Global Overview page (harmless if
    # injected twice — Streamlit/CSS just re-applies the same rule).
    st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1.25rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    actual     = D["actual"]
    actual_comp= D["actual_comp"]
    domain_change = D["domain_change"]

    # Row 0: filters inline with no spacer 

    f0 = st.columns([1.8, 1.8, 8])

    with f0[0]:
        reg_opts = ["All Regions"] + sorted(actual["Region"].dropna().unique().tolist())
        sel_reg = st.selectbox("Region", reg_opts, key="p2_reg", label_visibility="visible")

    with f0[1]:
        yr_opts = sorted(actual["Year"].unique().tolist(), reverse=True)
        sel_yr = st.selectbox("Year", yr_opts, index=0, key="p2_yr", label_visibility="visible")

    act_yr = actual[actual["Year"] == sel_yr]
    act_yr_f = act_yr if sel_reg == "All Regions" else act_yr[act_yr["Region"] == sel_reg]
    domain_avgs = act_yr_f.groupby("Domain")["Domain_Score"].mean()

    # Row 1: Domain cards
    dcols = st.columns(6)
    for i, dom in enumerate(DOMAINS):
        score = float(domain_avgs.get(dom, 0.0))
        dc    = DOMAIN_COLORS.get(dom, "#94A3B8")
        icon  = DOMAIN_ICONS.get(dom, "")
        ch_row = domain_change[domain_change["Domain"] == dom]
        chg    = float(ch_row["Change"].values[0]) if not ch_row.empty else 0.0
        t_arrow  = "↑" if chg >= 0 else "↓"
        t_color  = "#34D399" if chg >= 0 else "#F87171"
        _DOM_ABBREV = {
            "Climate & Energy": "Climate",
            "Digital Infrastructure": "Digital Infra",
            "Economic Fragility": "Economic",
            "Food Security": "Food",
            "Healthcare": "Healthcare",
            "Political Stability": "Political",
        }
        short = _DOM_ABBREV.get(dom, dom[:12])
        dcols[i].markdown(f"""
<div style="background:#192133;border:1px solid #263354;border-left:3px solid {dc};
            border-radius:6px;padding:8px 11px;height:78px;overflow:hidden;">
  <div style="font-size:15px;line-height:1;">{icon}</div>
  <div style="font-size:8px;color:#94A3B8;font-weight:600;text-transform:uppercase;
              letter-spacing:0.05em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;"
       title="{dom}">{short}</div>
  <div style="font-size:20px;font-weight:700;color:{dc};
              font-family:'JetBrains Mono',monospace;line-height:1.2;">{score:.3f}</div>
  <div style="font-size:9px;color:{t_color};">{t_arrow} {chg:+.3f} vs {D["base_yr"]}</div>
</div>""", unsafe_allow_html=True)

    # Row 2: Radar | Heatmap
    r_col, h_col = st.columns([3, 8])

    # Radar
    with r_col:
        gvals = [float(domain_avgs.get(d, 0)) for d in DOMAINS]
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatterpolar(
            r=gvals + [gvals[0]], theta=DOMAINS + [DOMAINS[0]],
            fill="toself", fillcolor="rgba(56,189,248,0.1)",
            line=dict(color="#38BDF8", width=2),
            name="Selected" if sel_reg != "All Regions" else "Global Avg",
        ))
        if sel_reg != "All Regions":
            all_avgs = act_yr.groupby("Domain")["Domain_Score"].mean()
            gv2 = [float(all_avgs.get(d, 0)) for d in DOMAINS]
            fig_r.add_trace(go.Scatterpolar(
                r=gv2 + [gv2[0]], theta=DOMAINS + [DOMAINS[0]],
                fill="toself", fillcolor="rgba(129,140,248,0.07)",
                line=dict(color="#818CF8", width=1.5, dash="dot"),
                name="Global",
            ))
        fig_r.update_layout(
            **base_layout(),
            height=270,
            margin=dict(t=55, b=28, l=28, r=28),
            title=dict(text="Domain Radar", font=dict(size=11, color="#94A3B8"), x=0.01),
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                angularaxis=dict(color="#94A3B8", gridcolor="#263354",
                                 tickfont=dict(size=8, color="#94A3B8")),
                radialaxis=dict(visible=True, range=[0,1], gridcolor="#263354",
                                tickfont=dict(size=7, color="#94A3B8"), color="#94A3B8",
                                tickvals=[0.25,0.5,0.75]),
            ),
            showlegend=True,
            legend=dict(orientation="h", y=-0.06, font=dict(size=9, color="#94A3B8")),
        )
        st.plotly_chart(fig_r, use_container_width=True, config={"displayModeBar": False})

    # Heatmap
    with h_col:
        dr_src = (act_yr_f if sel_reg != "All Regions" else act_yr)
        dr_data = dr_src.groupby(["Region","Domain"])["Domain_Score"].mean().reset_index()
        if not dr_data.empty:
            pivot = dr_data.pivot(index="Region", columns="Domain", values="Domain_Score")
            pivot = pivot.reindex(columns=[d for d in DOMAINS if d in pivot.columns])
            pivot = pivot.loc[pivot.mean(axis=1).sort_values(ascending=False).index]
            _HMAP_ABBREV = {
                "Climate & Energy": "Climate",
                "Digital Infrastructure": "Digital",
                "Economic Fragility": "Economic",
                "Food Security": "Food",
                "Healthcare": "Healthcare",
                "Political Stability": "Political",
            }
            x_lab = [_HMAP_ABBREV.get(c, c) for c in pivot.columns]
            z_vals = pivot.values
            txt_vals = [[f"{v:.2f}" if not np.isnan(v) else "" for v in row] for row in z_vals]
            fig_h = go.Figure(go.Heatmap(
                z=z_vals, x=x_lab, y=pivot.index.tolist(),
                colorscale=[[0,"#F87171"],[0.4,"#FBBF24"],[0.7,"#38BDF8"],[1,"#34D399"]],
                zmin=0, zmax=1,
                text=txt_vals, texttemplate="%{text}",
                textfont={"size":10,"color":"white"},
                hoverongaps=False,
                colorbar=dict(thickness=10,len=0.85,tickfont=dict(size=8,color="#94A3B8")),
            ))
            fig_h.update_layout(
                **base_layout(),
                height=270,
                margin=dict(t=55, b=24, l=100, r=16),
                title=dict(text="Domain Performance by Region", font=dict(size=11,color="#94A3B8"), x=0.01),
                xaxis=dict(tickfont=dict(size=9,color="#94A3B8"), tickangle=-20,
                           gridcolor="#263354", linecolor="#263354"),
                yaxis=dict(tickfont=dict(size=9,color="#E2E8F0"), gridcolor="#263354", linecolor="#263354"),
            )
            st.plotly_chart(fig_h, use_container_width=True, config={"displayModeBar": False})


    # Row 3: Domain Trends Over Time | EDA Notebook Findings
    t_col, i_col = st.columns([7, 5])

    with t_col:
        act_reg = actual if sel_reg == "All Regions" else actual[actual["Region"] == sel_reg]
        dom_trend = act_reg.groupby(["Year", "Domain"])["Domain_Score"].mean().reset_index()
        fig_tr = go.Figure()
        for dom in DOMAINS:
            dt = dom_trend[dom_trend["Domain"] == dom].sort_values("Year")
            if not dt.empty:
                fig_tr.add_trace(go.Scatter(
                    x=dt["Year"], y=dt["Domain_Score"],
                    name=f"{DOMAIN_ICONS.get(dom,'')} {dom}",
                    line=dict(color=DOMAIN_COLORS.get(dom,"#94A3B8"), width=2),
                    hovertemplate=f"<b>{dom}</b> %{{x}}: %{{y:.3f}}<extra></extra>",
                ))
        reg_note = "" if sel_reg == "All Regions" else f" — {sel_reg}"
        fig_tr.update_layout(
            **base_layout(),
            height=260,  # shrunk to eliminate the page scrollbar; matches the EDA box height exactly
            margin=dict(t=28, b=40, l=38, r=10),
            title=dict(text=f"Domain Trends Over Time{reg_note} ({D['base_yr']}–{D['latest_yr']})",
                       font=dict(size=11, color="#94A3B8"), x=0.01),
            xaxis=dict(**styled_axis()),
            yaxis=dict(range=[0, 1.05], **styled_axis(), dtick=0.25),
            hovermode="x unified",
            legend=dict(orientation="h", y=-0.22, x=0, font=dict(size=8.5, color="#94A3B8"), bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_tr, use_container_width=True, config={"displayModeBar": False})

    with i_col:
        # Findings sourced from the Analysis Notebook, grounded in live figures
        vol_by_yr = actual.groupby(["Domain", "Year"])["Domain_Score"].mean().reset_index()
        vol_std   = vol_by_yr.groupby("Domain")["Domain_Score"].std().sort_values(ascending=False)
        most_volatile = vol_std.index[0] if not vol_std.empty else "Political Stability"

        strongest_grower = (domain_change.loc[domain_change["Change"].idxmax(), "Domain"]
                             if not domain_change.empty else "Digital Infrastructure")

        spread_latest = act_yr.groupby("Domain")["Domain_Score"].agg(lambda s: s.max() - s.min())
        widest_gap = spread_latest.idxmax() if not spread_latest.empty else "Healthcare"

        findings = [
            (most_volatile, "Weakest & most volatile domain across the full time series", "#F87171"),
            (strongest_grower, f"Strongest long-term improvement since {D['base_yr']}", "#34D399"),
            (widest_gap, f"Widest gap between top and bottom performers in {sel_yr}", "#FBBF24"),
        ]
        rows_html = ""
        for idx, (name, desc, clr) in enumerate(findings):
            ic = DOMAIN_ICONS.get(name, "")
            border = "border-bottom:1px solid #1E2A40;" if idx < len(findings) - 1 else ""
            rows_html += f"""
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;
            padding:8px 0;{border}">
  <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
    <span style="font-size:15px;">{ic}</span>
    <span style="font-size:12.5px;font-weight:700;color:{clr};">{name}</span>
  </div>
  <div style="font-size:11px;color:#94A3B8;line-height:1.4;">{desc}</div>
</div>"""
        # Fixed height (matches the Domain Trends chart height exactly) + flexbox
        # distribution + box-sizing:border-box so padding is included in that
        # height — this is what removes both the leftover whitespace and the
        # page-level vertical scrollbar.
        st.markdown(f"""
<div style="background:#192133;border:1px solid #263354;border-radius:6px;
            padding:10px 16px;height:230px;box-sizing:border-box;
            display:flex;flex-direction:column;overflow:hidden;">
  <div style="font-size:9px;color:#94A3B8;font-weight:600;letter-spacing:0.1em;
              text-transform:uppercase;margin-bottom:2px;">📌 EDA NOTEBOOK FINDINGS</div>
  {rows_html}
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 7. PAGE 3 — COUNTRY EXPLORER
# ─────────────────────────────────────────────────────────────────────────────

def page_country_explorer(D):
    actual      = D["actual"]
    actual_comp = D["actual_comp"]
    reg_trend   = D["regional_trend"]
    glob_trend  = D["global_trend"]
    latest      = D["latest"]

    countries = sorted(actual_comp["Country Name"].dropna().unique().tolist())
    def_idx   = countries.index("Switzerland") if "Switzerland" in countries else 0

    # Row 0: controls
    c0 = st.columns([4, 5, 3])
    with c0[0]:
        sel_c = st.selectbox("🔍 Select Country", countries, index=def_idx,
                             key="p3_country", label_visibility="visible")
    with c0[1]:
        yr_range = st.slider("Year Range", D["base_yr"], D["latest_yr"],
                             (D["base_yr"], D["latest_yr"]), key="p3_yrs",
                             label_visibility="visible")
    with c0[2]:
        cinfo = actual_comp[actual_comp["Country Name"] == sel_c]
        region = cinfo.iloc[0]["Region"] if not cinfo.empty else "Unknown"
        ccode  = cinfo.iloc[0]["Country Code"] if not cinfo.empty else ""
        rc     = REGION_COLORS.get(region, "#94A3B8")
        st.markdown(f'<div style="padding-top:20px;">'
                    f'<span style="background:{rc}22;color:{rc};border:1px solid {rc}44;'
                    f'border-radius:4px;padding:3px 10px;font-size:11px;font-weight:600;">'
                    f'{region}</span></div>', unsafe_allow_html=True)

    # Filtered data
    c_ts = actual_comp[
        (actual_comp["Country Name"] == sel_c) &
        (actual_comp["Year"] >= yr_range[0]) &
        (actual_comp["Year"] <= yr_range[1])
    ].sort_values("Year")
    r_ts = reg_trend[
        (reg_trend["Region"] == region) &
        (reg_trend["Year"] >= yr_range[0]) &
        (reg_trend["Year"] <= yr_range[1])
    ]
    g_ts = glob_trend[
        (glob_trend["Year"] >= yr_range[0]) &
        (glob_trend["Year"] <= yr_range[1])
    ]
    c_dom_2023 = actual[
        (actual["Country Name"] == sel_c) & (actual["Year"] == D["latest_yr"])
    ]
    lat_row = latest[latest["Country Name"] == sel_c]
    score_2023 = float(lat_row["Composite_Score"].values[0]) if not lat_row.empty else 0.0
    rank_2023  = int(lat_row["Rank"].values[0])               if not lat_row.empty else 0
    tier_val   = assign_tier(score_2023)
    risk_val   = assign_risk(score_2023)
    tc         = tier_color(tier_val)
    rc2        = risk_color(risk_val)
    flag       = get_flag(ccode)

    # Row 1: Country Card | Trend | Story
    r1a, r1b, r1c = st.columns([2, 5.5, 2.5])

    with r1a:
        st.markdown(f"""
<div style="background:#192133;border:1px solid #263354;border-left:4px solid #38BDF8;
            border-radius:6px;padding:14px 14px;min-height:280px;">
  <div style="font-size:30px;line-height:1;">{flag}</div>
  <div style="font-size:14px;font-weight:700;color:#E2E8F0;margin-top:4px;
              white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{sel_c}</div>
  <div style="font-size:9px;color:#94A3B8;margin-bottom:6px;">{region}</div>
  <div style="font-size:28px;font-weight:700;color:#38BDF8;
              font-family:'JetBrains Mono',monospace;line-height:1.1;">{score_2023:.3f}</div>
  <div style="font-size:8px;color:#94A3B8;margin-bottom:9px;">Overall Score {D["latest_yr"]}</div>
  <div style="display:flex;gap:4px;flex-wrap:wrap;">
    {badge(f"#{rank_2023}")}
    <span style="background:{tc}22;color:{tc};border:1px solid {tc}33;border-radius:4px;
                 padding:2px 7px;font-size:9px;font-weight:600;">Tier {tier_val}</span>
    <span style="background:{rc2}22;color:{rc2};border:1px solid {rc2}33;border-radius:4px;
                 padding:2px 7px;font-size:9px;font-weight:600;">{risk_val}</span>
  </div>
</div>""", unsafe_allow_html=True)

    with r1b:
        fig_t = go.Figure()
        if not c_ts.empty:
            fig_t.add_trace(go.Scatter(
                x=c_ts["Year"], y=c_ts["Composite_Score"], name=sel_c[:18],
                line=dict(color="#38BDF8", width=2.5),
                fill="tozeroy", fillcolor="rgba(56,189,248,0.06)",
                hovertemplate="<b>%{x}</b>: %{y:.3f}<extra></extra>",
            ))
        if not r_ts.empty:
            fig_t.add_trace(go.Scatter(
                x=r_ts["Year"], y=r_ts["Composite_Score"],
                name=f"{region} Avg",
                line=dict(color=REGION_COLORS.get(region,"#94A3B8"), width=1.5, dash="dot"),
                hovertemplate="<b>%{x}</b>: %{y:.3f}<extra></extra>",
            ))
        if not g_ts.empty:
            fig_t.add_trace(go.Scatter(
                x=g_ts["Year"], y=g_ts["Composite_Score"], name="Global Avg",
                line=dict(color="#94A3B8", width=1, dash="dash"),
                hovertemplate="<b>%{x}</b>: %{y:.3f}<extra></extra>",
            ))
        # Peak/trough annotations
        if not c_ts.empty and len(c_ts) > 1:
            pk  = c_ts.loc[c_ts["Composite_Score"].idxmax()]
            tr  = c_ts.loc[c_ts["Composite_Score"].idxmin()]
            fig_t.add_annotation(x=pk["Year"], y=pk["Composite_Score"],
                text=f"▲{pk['Composite_Score']:.3f}", showarrow=True,
                arrowhead=2, arrowsize=0.8, arrowwidth=1,
                font=dict(size=8,color="#34D399"), arrowcolor="#34D399",
                ay=-22, bgcolor="rgba(25,33,51,0.85)", bordercolor="#34D399")
            if int(tr["Year"]) != int(pk["Year"]):
                fig_t.add_annotation(x=tr["Year"], y=tr["Composite_Score"],
                    text=f"▼{tr['Composite_Score']:.3f}", showarrow=True,
                    arrowhead=2, arrowsize=0.8, arrowwidth=1,
                    font=dict(size=8,color="#F87171"), arrowcolor="#F87171",
                    ay=22, bgcolor="rgba(25,33,51,0.85)", bordercolor="#F87171")
        fig_t.update_layout(
            **base_layout(),
            height=280,
            margin=dict(t=28, b=26, l=38, r=10),
            title=dict(text="Composite Score Over Time", font=dict(size=11,color="#94A3B8"), x=0.01),
            xaxis=dict(**styled_axis()),
            yaxis=dict(range=[0,1.05], **styled_axis(), dtick=0.25),
            hovermode="x unified",
            legend=dict(orientation="h", x=0, y=-0.12, font=dict(size=9,color="#94A3B8"), bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_t, use_container_width=True, config={"displayModeBar": False})

    with r1c:
        # Story text
        if not c_ts.empty and len(c_ts) >= 2:
            s_val = float(c_ts.iloc[0]["Composite_Score"])
            e_val = float(c_ts.iloc[-1]["Composite_Score"])
            chg   = e_val - s_val
            dirc  = "improved" if chg > 0 else "declined"
            dc    = "#34D399" if chg > 0 else "#F87171"
            pk    = c_ts.loc[c_ts["Composite_Score"].idxmax()]
            tr    = c_ts.loc[c_ts["Composite_Score"].idxmin()]
            bd    = c_dom_2023.loc[c_dom_2023["Domain_Score"].idxmax()]["Domain"] if not c_dom_2023.empty else "—"
            wd    = c_dom_2023.loc[c_dom_2023["Domain_Score"].idxmin()]["Domain"] if not c_dom_2023.empty else "—"
            story = (f'<b>{sel_c}</b> has <b style="color:{dc};">{dirc}</b> by '
                     f'<b style="font-family:\'JetBrains Mono\',monospace;">{abs(chg):.3f}</b> pts '
                     f'({int(c_ts.iloc[0]["Year"])}→{int(c_ts.iloc[-1]["Year"])}).<br><br>'
                     f'Peak: <b>{int(pk["Year"])}</b> ({pk["Composite_Score"]:.3f}) &nbsp; '
                     f'Low: <b>{int(tr["Year"])}</b> ({tr["Composite_Score"]:.3f}).<br><br>'
                     f'Strongest: <b style="color:#34D399;">{DOMAIN_ICONS.get(bd,"")} {bd}</b><br>'
                     f'Gap: <b style="color:#F87171;">{DOMAIN_ICONS.get(wd,"")} {wd}</b>')
        else:
            story = f"<b>{sel_c}</b>: Insufficient historical data."
        st.markdown(f"""
<div style="background:#192133;border:1px solid #263354;border-radius:6px;
            padding:14px 14px;min-height:220px;">
  <div style="font-size:10px;color:#94A3B8;font-weight:600;letter-spacing:0.1em;
              text-transform:uppercase;margin-bottom:8px;">📖 HISTORICAL NARRATIVE</div>
  <div style="font-size:11px;color:#E2E8F0;line-height:1.65;">{story}</div>
</div>""", unsafe_allow_html=True)

    # Row 2: Radar | Domain Lines | Rank Tracker — match row 1 heights
    r2a, r2b, r2c = st.columns([3, 5, 3])

    with r2a:
        dsc = {r["Domain"]: r["Domain_Score"] for _, r in c_dom_2023.iterrows()}
        rv  = [float(dsc.get(d, 0)) for d in DOMAINS]
        fig_rad = go.Figure(go.Scatterpolar(
            r=rv + [rv[0]], theta=DOMAINS + [DOMAINS[0]],
            fill="toself", fillcolor="rgba(56,189,248,0.1)",
            line=dict(color="#38BDF8", width=2),
        ))
        fig_rad.update_layout(
            **base_layout(),
            height=280,
            margin=dict(t=24, b=6, l=28, r=28),
            title=dict(text=f"Domain Profile {D['latest_yr']}", font=dict(size=10,color="#94A3B8"), x=0.01),
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                angularaxis=dict(color="#94A3B8", gridcolor="#263354",
                                 tickfont=dict(size=7.5,color="#94A3B8")),
                radialaxis=dict(visible=True, range=[0,1], gridcolor="#263354",
                                tickfont=dict(size=6.5,color="#94A3B8"), color="#94A3B8",
                                tickvals=[0.25,0.5,0.75]),
            ),
            showlegend=False,
        )
        st.plotly_chart(fig_rad, use_container_width=True, config={"displayModeBar": False})

    with r2b:
        c_dom_ts = actual[
            (actual["Country Name"] == sel_c) &
            (actual["Year"] >= yr_range[0]) &
            (actual["Year"] <= yr_range[1])
        ]
        fig_d = go.Figure()
        for dom in DOMAINS:
            d_ts = c_dom_ts[c_dom_ts["Domain"] == dom].sort_values("Year")
            if not d_ts.empty:
                fig_d.add_trace(go.Scatter(
                    x=d_ts["Year"], y=d_ts["Domain_Score"],
                    name=f"{DOMAIN_ICONS.get(dom,'')} {dom}",
                    line=dict(color=DOMAIN_COLORS.get(dom,"#94A3B8"), width=1.8),
                    hovertemplate=f"<b>{dom}</b>: %{{y:.3f}}<extra></extra>",
                ))
        fig_d.update_layout(
            **base_layout(),
            height=280,
            margin=dict(t=24, b=72, l=38, r=10),
            title=dict(text="Domain Scores Over Time", font=dict(size=11,color="#94A3B8"), x=0.01),
            xaxis=dict(**styled_axis()),
            yaxis=dict(range=[0,1.05], **styled_axis(), dtick=0.25),
            hovermode="x unified",
            legend=dict(orientation="h", y=-0.28, font=dict(size=8,color="#94A3B8"),
                        bgcolor="rgba(0,0,0,0)", x=0),
        )
        st.plotly_chart(fig_d, use_container_width=True, config={"displayModeBar": False})

    with r2c:
        ranks = []
        for yr in range(yr_range[0], yr_range[1]+1):
            ydf = actual_comp[actual_comp["Year"]==yr].copy()
            if ydf.empty: continue
            ydf["_Rank"] = ydf["Composite_Score"].rank(ascending=False, method="min").astype(int)
            row = ydf[ydf["Country Name"]==sel_c]
            if not row.empty:
                ranks.append({"Year": yr, "Rank": int(row.iloc[0]["_Rank"])})
        rank_df = pd.DataFrame(ranks)
        fig_rk = go.Figure()
        if not rank_df.empty:
            fig_rk.add_trace(go.Scatter(
                x=rank_df["Year"], y=rank_df["Rank"],
                line=dict(color="#818CF8", width=2),
                fill="tozeroy", fillcolor="rgba(129,140,248,0.06)",
                hovertemplate="<b>%{x}</b>: Rank #%{y}<extra></extra>",
            ))
            for ann_r, ay_off in [(rank_df.iloc[0], -16), (rank_df.iloc[-1], -16)]:
                fig_rk.add_annotation(
                    x=ann_r["Year"], y=ann_r["Rank"],
                    text=f"#{int(ann_r['Rank'])}", showarrow=False,
                    font=dict(size=9,color="#818CF8"),
                    bgcolor="rgba(25,33,51,0.9)", bordercolor="#818CF8",
                    yshift=ay_off,
                )
        fig_rk.update_layout(
            **base_layout(),
            height=280,
            margin=dict(t=50, b=26, l=38, r=10),
            title=dict(text="Global Rank Over Time", font=dict(size=11,color="#94A3B8"), x=0.01),
            xaxis=dict(**styled_axis()),
            yaxis=dict(autorange="reversed", **styled_axis(),
                       title=dict(text="Rank", font=dict(size=9,color="#94A3B8"))),
        )
        st.plotly_chart(fig_rk, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────────────────────────────────────────
# 8. PAGE 4 — RISK & OPPORTUNITY
# ─────────────────────────────────────────────────────────────────────────────

def page_risk_opportunity(D):
    change_df = D["change_df"].copy()
    actual    = D["actual"]

    if "p4_sel" not in st.session_state:
        st.session_state["p4_sel"] = None

    # Row 0: filters — all inline, compact, no spacer column
    f0 = st.columns([1.5, 1.5, 3, 2])
    with f0[0]:
        reg_opts = ["All Regions"] + sorted(change_df["Region"].dropna().unique().tolist())
        sel_reg  = st.selectbox("Region", reg_opts, key="p4_reg", label_visibility="visible")
    with f0[1]:
        risk_opts = ["All Levels","Critical","High","Medium","Low"]
        sel_risk  = st.selectbox("Risk Level", risk_opts, key="p4_risk", label_visibility="visible")
    with f0[2]:
        country_pick_opts = ["(Global View)"] + sorted(change_df["Country Name"].tolist())
        sel_pick = st.selectbox("Focus Country", country_pick_opts, key="p4_pick", label_visibility="visible")
        if sel_pick != "(Global View)":
            st.session_state["p4_sel"] = sel_pick

    # Filter
    df = change_df.copy()
    if sel_reg != "All Regions":
        df = df[df["Region"] == sel_reg]
    if sel_risk != "All Levels":
        df = df[df["Risk"] == sel_risk]

    # Row 1: KPIs
    kc = st.columns(4)
    if not df.empty:
        hr  = (df["Risk"].isin(["High","Critical"])).sum()
        imp = (df["Score_Change"] > 0).sum()
        dec = (df["Score_Change"] < 0).sum()
        crit = (df["Score_2023"] < 0.35).sum()
        kc[0].markdown(kpi("High / Critical Risk", str(hr), f"of {len(df)} countries", "#F87171"), unsafe_allow_html=True)
        kc[1].markdown(kpi("Improving", str(imp), "Score change > 0", "#34D399"), unsafe_allow_html=True)
        kc[2].markdown(kpi("Declining", str(dec), "Score change < 0", "#FBBF24"), unsafe_allow_html=True)
        kc[3].markdown(kpi("Critical Fragile", str(crit), "Score below 0.35", "#DC2626"), unsafe_allow_html=True)
    else:
        for col in kc: col.markdown(kpi("No Data","—",""), unsafe_allow_html=True)

    # Row 2: Scatter | Movers
    sc_col, mv_col = st.columns([7.5, 2.5])

    with sc_col:
        if not df.empty:
            fig_s = px.scatter(
                df, x="Score_2023", y="Score_Change",
                color="Region", color_discrete_map=REGION_COLORS,
                hover_name="Country Name",
                hover_data={"Score_2023":":.3f","Score_Change":":.3f","Region":True,"Tier":True,"Risk":True},
            )
            fig_s.update_traces(marker=dict(size=8, opacity=0.85, line=dict(width=0)))
            fig_s.add_hline(y=0,  line=dict(color="#38BDF8", dash="dash", width=1), opacity=0.35)
            fig_s.add_vline(x=0.55, line=dict(color="#38BDF8", dash="dash", width=1), opacity=0.35)
            # Highlight selected
            sel_name = st.session_state.get("p4_sel")
            if sel_name and sel_name in df["Country Name"].values:
                sel_row = df[df["Country Name"]==sel_name].iloc[0]
                fig_s.add_trace(go.Scatter(
                    x=[sel_row["Score_2023"]], y=[sel_row["Score_Change"]],
                    mode="markers+text",
                    marker=dict(size=14, color="#FBBF24", symbol="circle-open", line=dict(width=2.5, color="#FBBF24")),
                    text=[sel_name[:14]], textposition="top center",
                    textfont=dict(size=9, color="#FBBF24"),
                    showlegend=False,
                    hovertemplate=f"<b>{sel_name}</b><extra></extra>",
                ))
            x_min, x_max = df["Score_2023"].min()-0.03, df["Score_2023"].max()+0.03
            y_min, y_max = df["Score_Change"].min()-0.01, df["Score_Change"].max()+0.01
            for txt, x, y, anch in [
                ("Improving & Resilient",     x_max-0.01, y_max-0.005, "right"),
                ("Declining Despite Strength",x_max-0.01, y_min+0.005, "right"),
                ("Recovering Fragile",        0.50,       y_max-0.005, "right"),
                ("High Risk — Declining",     0.50,       y_min+0.005, "right"),
            ]:
                fig_s.add_annotation(text=txt, x=x, y=y, showarrow=False,
                    font=dict(size=8,color="#5A6B85"), xanchor=anch)
            fig_s.update_layout(
                **base_layout(),
                height=400,
                margin=dict(t=55, b=56, l=46, r=12),
                title=dict(text="Risk Matrix — Composite Score vs Change (2000→2023)", font=dict(size=11,color="#94A3B8"), x=0.01),
                xaxis=dict(title=dict(text="Composite Score 2023",font=dict(size=9,color="#94A3B8")),
                           range=[x_min,x_max], **styled_axis()),
                yaxis=dict(title=dict(text="Score Change",font=dict(size=9,color="#94A3B8")),
                           range=[y_min,y_max], **styled_axis()),
                legend=dict(orientation="h", y=-0.18, font=dict(size=9,color="#94A3B8"), bgcolor="rgba(0,0,0,0)"),
            )
            event = st.plotly_chart(fig_s, use_container_width=True,
                                    config={"displayModeBar": False},
                                    key="p4_scatter", on_select="rerun",
                                    selection_mode="points")
            if event and hasattr(event,"selection") and event.selection:
                pts = event.selection.get("points",[])
                if pts:
                    px_val = pts[0].get("x")
                    py_val = pts[0].get("y")
                    if px_val is not None and py_val is not None:
                        close = df[
                            (abs(df["Score_2023"]-px_val)<0.002) &
                            (abs(df["Score_Change"]-py_val)<0.002)
                        ]
                        if not close.empty:
                            st.session_state["p4_sel"] = close.iloc[0]["Country Name"]

    with mv_col:
        st.markdown(
    '<div style="padding-top:16px;'
    'font-size:11px;'
    'color:#34D399;'
    'font-weight:1000;'
    'letter-spacing:0.15em;'
    'text-transform:uppercase;'
    'margin-bottom:10px;">'
    '↑ TOP IMPROVERS</div>',
    unsafe_allow_html=True
)
        if not df.empty:
            def movers_html(sub_df, is_top):
                clr = "#34D399" if is_top else "#F87171"
                arr = "↑" if is_top else "↓"
                rows = ""
                for _, r in sub_df.iterrows():
                    cname = r["Country Name"]
                    rows += (f'<tr style="border-bottom:2px solid #1E2A40;">'
                             f'<td style="font-size:10px;color:#E2E8F0;padding:6px 8px;'
                             f'max-width:130px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;"'
                             f' title="{cname}">{cname}</td>'
                             f'<td style="font-size:10px;color:{clr};font-family:\'JetBrains Mono\',monospace;'
                             f'padding:6px 8px;text-align:right;white-space:nowrap;">{arr} {abs(r["Score_Change"]):.3f}</td></tr>')
                return f'<table style="width:100%;border-collapse:collapse;">{rows}</table>'

            st.markdown(f'<div style="background:#192133;border:2px solid #263354;border-radius:14px;'
                        f'padding:14px;margin-bottom:10px;">'
                        f'{movers_html(df.nlargest(5,"Score_Change"), True)}</div>',
                        unsafe_allow_html=True)
            st.markdown(
                '<div style="padding-top:16px;'
                'font-size:11px;'
                'color:#F87171;'
                'font-weight:1000;'
                'letter-spacing:0.15em;'
                'text-transform:uppercase;'
                'margin-bottom:10px;">'
                '↓ TOP DECLINERS</div>',
                unsafe_allow_html=True
            )
            st.markdown(f'<div style="background:#192133;border:2px solid #263354;border-radius:14px;'
                        f'padding:12px;margin-bottom:8px;">'
                        f'{movers_html(df.nsmallest(5,"Score_Change"), False)}</div>',
                        unsafe_allow_html=True)

    # Row 3: Strategic Insight Panel
    sel_name = st.session_state.get("p4_sel")
    if sel_name and sel_name in change_df["Country Name"].values:
        c_row = change_df[change_df["Country Name"]==sel_name].iloc[0]
        c_score = float(c_row["Score_2023"])
        c_chg   = float(c_row["Score_Change"])
        c_reg   = str(c_row["Region"])
        c_doms  = actual[(actual["Country Name"]==sel_name) & (actual["Year"]==D["latest_yr"])]

        bd = c_doms.loc[c_doms["Domain_Score"].idxmax()]["Domain"] if not c_doms.empty else "—"
        wd = c_doms.loc[c_doms["Domain_Score"].idxmin()]["Domain"] if not c_doms.empty else "—"
        bd_s = float(c_doms.loc[c_doms["Domain_Score"].idxmax()]["Domain_Score"]) if not c_doms.empty else 0
        wd_s = float(c_doms.loc[c_doms["Domain_Score"].idxmin()]["Domain_Score"]) if not c_doms.empty else 0

        s1 = (f'{DOMAIN_ICONS.get(bd,"")} <b>{bd}</b> '
              f'<span style="font-family:\'JetBrains Mono\',monospace;color:#34D399;">({bd_s:.2f})</span>')
        s2 = (f'{DOMAIN_ICONS.get(wd,"")} <b>{wd}</b> '
              f'<span style="font-family:\'JetBrains Mono\',monospace;color:#F87171;">({wd_s:.2f})</span>')
        dirc = "improving" if c_chg > 0 else "declining"
        s3   = (f'<b>{dirc.capitalize()}</b> by '
                f'<span style="font-family:\'JetBrains Mono\',monospace;">{abs(c_chg):.3f}</span> since 2000. '
                f'<b>{assign_risk(c_score)}</b> risk · Score '
                f'<span style="font-family:\'JetBrains Mono\',monospace;">{c_score:.3f}</span>')
        s4   = (f'<b>{sel_name}</b> holds a '
                f'<b>{"stable" if abs(c_chg)<0.05 else dirc}</b> trajectory in <b>{c_reg}</b>. '
                f'Lowest domain constrains overall index performance.')
        panel_title = f"📋 STRATEGIC INSIGHT — {sel_name.upper()}"
    else:
        df_gl = change_df.copy()
        imp_n = (df_gl["Score_Change"]>0).sum()
        dec_n = (df_gl["Score_Change"]<0).sum()
        top_i = df_gl.nlargest(1,"Score_Change").iloc[0]
        bot_i = df_gl.nsmallest(1,"Score_Change").iloc[0]
        s1 = (f'<b>{imp_n}</b> countries improving. Top: <b>{top_i["Country Name"]}</b> '
              f'<span style="font-family:\'JetBrains Mono\',monospace;color:#34D399;">(+{top_i["Score_Change"]:.3f})</span>')
        s2 = (f'<b>{dec_n}</b> countries declining. Worst: <b>{bot_i["Country Name"]}</b> '
              f'<span style="font-family:\'JetBrains Mono\',monospace;color:#F87171;">({bot_i["Score_Change"]:.3f})</span>')
        s3  = (f'<b>{(df_gl["Risk"].isin(["High","Critical"])).sum()}</b> countries at High/Critical risk. '
               f'Global avg: <span style="font-family:\'JetBrains Mono\',monospace;">'
               f'{df_gl["Score_2023"].mean():.3f}</span>')
        s4  = f'<b>{imp_n/(imp_n+dec_n)*100:.0f}%</b> of tracked countries have improved since 2000. Click a scatter point to inspect individual countries.'
        panel_title = "📋 GLOBAL STRATEGIC INTELLIGENCE"

    st.markdown(f"""
<div style="background:#192133;border:1px solid #263354;border-radius:8px;
            padding:11px 14px;margin-top:3px;">
  <div style="font-size:10px;color:#94A3B8;font-weight:600;letter-spacing:0.1em;
              text-transform:uppercase;margin-bottom:9px;">{panel_title}</div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:14px;">
    <div>
      <div style="font-size:14px;color:#34D399;font-weight:700;text-transform:uppercase;
                  letter-spacing:0.08em;margin-bottom:3px;">✅ STRENGTHS</div>
      <div style="font-size:12px;color:#E2E8F0;line-height:1.5;">{s1}</div>
    </div>
    <div style="border-left:1px solid #263354;padding-left:14px;">
      <div style="font-size:14px;color:#F87171;font-weight:700;text-transform:uppercase;
                  letter-spacing:0.08em;margin-bottom:3px;">⚠️ VULNERABILITIES</div>
      <div style="font-size:12px;color:#E2E8F0;line-height:1.5;">{s2}</div>
    </div>
    <div style="border-left:1px solid #263354;padding-left:14px;">
      <div style="font-size:14px;color:#FBBF24;font-weight:700;text-transform:uppercase;
                  letter-spacing:0.08em;margin-bottom:3px;">📊 RISK TRAJECTORY</div>
      <div style="font-size:12px;color:#E2E8F0;line-height:1.5;">{s3}</div>
    </div>
    <div style="border-left:1px solid #263354;padding-left:14px;">
      <div style="font-size:14px;color:#818CF8;font-weight:700;text-transform:uppercase;
                  letter-spacing:0.08em;margin-bottom:3px;">🔍 INSIGHT</div>
      <div style="font-size:12px;color:#E2E8F0;line-height:1.5;">{s4}</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 9. PAGE 5 — ESTIMATED EXPLORER
# ─────────────────────────────────────────────────────────────────────────────

def page_estimated_explorer(D):
    estimated   = D["estimated"]
    est_comp    = D["est_comp"]
    est_latest  = D["est_latest"].copy()

    # Filters — no wasted spacer column
    f0 = st.columns([2, 2, 2, 5])
    with f0[0]:
        reg_opts = ["All Regions"] + sorted(est_latest["Region"].dropna().unique().tolist())
        sel_reg  = st.selectbox("Region", reg_opts, key="p5_reg", label_visibility="visible")
    with f0[1]:
        risk_opts = ["All","Critical","High","Medium","Low"]
        sel_risk  = st.selectbox("Risk Level", risk_opts, key="p5_risk", label_visibility="visible")
    with f0[2]:
        est_yr_opts = sorted(est_comp["Year"].unique().tolist(), reverse=True)
        sel_est_yr  = st.selectbox("Year", est_yr_opts, index=0, key="p5_year", label_visibility="visible")

    # Recompute the estimated universe for the selected year (this filter affects only this page)
    year_est = est_comp[est_comp["Year"] == sel_est_yr].copy()
    year_est["Tier"] = year_est["Composite_Score"].apply(assign_tier)
    year_est["Risk"] = year_est["Composite_Score"].apply(assign_risk)

    df = year_est.copy()
    if sel_reg != "All Regions":
        df = df[df["Region"] == sel_reg]
    if sel_risk != "All":
        df = df[df["Risk"] == sel_risk]

    top10 = df.nlargest(10,"Composite_Score")
    bot10 = df.nsmallest(10,"Composite_Score")

    def list_item(row, is_top):
        fl   = get_flag(row["Country Code"])
        sc   = float(row["Composite_Score"])
        t    = assign_tier(sc)
        tc2  = tier_color(t)
        bc   = "#34D399" if is_top else "#F87171"
        return f"""
<div style="padding:5px 8px;border-bottom:1px solid #1E2A40;">
  <div style="display:flex;align-items:center;gap:7px;margin-bottom:2px;">
    <span style="font-size:14px;">{fl}</span>
    <div style="flex:1;min-width:0;">
      <div style="font-size:10px;font-weight:600;color:#E2E8F0;white-space:nowrap;
                  overflow:hidden;text-overflow:ellipsis;">{row["Country Name"]}</div>
      <div style="font-size:8px;color:#94A3B8;">{row["Region"]}</div>
    </div>
    <div style="text-align:right;">
      <div style="font-size:11.5px;font-weight:700;color:{bc};
                  font-family:'JetBrains Mono',monospace;">{sc:.3f}</div>
      <span style="font-size:7.5px;color:{tc2};background:{tc2}22;
                   border-radius:3px;padding:1px 4px;">T{t}</span>
    </div>
  </div>
  {pbr(sc, bc, 2)}
</div>"""

    lc, cc, rc = st.columns([3, 4, 3])

    with lc:
        items = "".join(list_item(r, True) for _, r in top10.iterrows())
        st.markdown(f"""
<div style="background:#192133;border:1px solid #263354;border-radius:8px;overflow:hidden;height:530px;">
  <div style="padding:9px 11px;background:#1E2A40;border-bottom:1px solid #263354;">
    <span style="font-size:10px;color:#34D399;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;">
      🏆 TOP 10 — ESTIMATED COUNTRIES ({sel_est_yr})</span>
  </div>
  <div style="overflow-y:auto;max-height:485px;">{items}</div>
</div>""", unsafe_allow_html=True)

    with cc:
        all_c = sorted(df["Country Name"].tolist()) if not df.empty else []
        if not all_c:
            st.markdown('<div style="background:#192133;border:1px solid #263354;border-radius:8px;'
                        'padding:40px;text-align:center;color:#94A3B8;height:530px;">'
                        'No countries match filters.</div>', unsafe_allow_html=True)
        else:
            # Default to a high-scoring estimated country
            def_name = top10.iloc[0]["Country Name"] if not top10.empty else all_c[0]
            def_idx  = all_c.index(def_name) if def_name in all_c else 0
            sel_est  = st.selectbox("🔍 Select Estimated Country", all_c, index=def_idx,
                                    key="p5_country", label_visibility="visible")
            crow = df[df["Country Name"]==sel_est]
            if crow.empty:
                crow = year_est[year_est["Country Name"]==sel_est]

            if not crow.empty:
                cr  = crow.iloc[0]
                fl  = get_flag(cr["Country Code"])
                sc  = float(cr["Composite_Score"])
                t   = assign_tier(sc)
                ri  = assign_risk(sc)
                tc2 = tier_color(t)
                rc2 = risk_color(ri)
                # Estimated countries have no actual reported data for this indicator set
                c_dom_est = estimated[(estimated["Country Name"]==sel_est) & (estimated["Year"]==sel_est_yr)]

                dom_rows = ""
                for dom in DOMAINS:
                    dr = c_dom_est[c_dom_est["Domain"]==dom]
                    has_data = not dr.empty and not pd.isna(dr["Domain_Score"].values[0])
                    ds = float(dr["Domain_Score"].values[0]) if has_data else None
                    dc2 = DOMAIN_COLORS.get(dom,"#94A3B8")
                    if ds is None or ds == 0.0 and not has_data:
                        score_display = '<span style="font-size:10px;color:#64748B;font-style:italic;">N/A</span>'
                        bar_html = f'<div style="background:#1E2A40;border-radius:2px;height:4px;width:100%;margin-top:3px;"></div>'
                    else:
                        score_display = f'<span style="font-size:10.5px;color:{dc2};font-family:\'JetBrains Mono\',monospace;">{ds:.3f}</span>'
                        bar_html = pbr(ds, dc2, 4)
                    dom_rows += (f'<div style="margin-bottom:10px;">'
                                 f'<div style="display:flex;justify-content:space-between;margin-bottom:2px;">'
                                 f'<span style="font-size:10.5px;color:#E2E8F0;">'
                                 f'{DOMAIN_ICONS.get(dom,"")} {dom}</span>'
                                 f'{score_display}</div>'
                                 f'{bar_html}</div>')

                st.markdown(f"""
<div style="background:#192133;border:1px solid #263354;border-top:4px solid #818CF8;
            border-radius:8px;padding:16px;height:480px;overflow:hidden;">
  <div style="display:flex;align-items:center;gap:11px;margin-bottom:13px;
              padding-bottom:11px;border-bottom:1px solid #263354;">
    <div style="font-size:34px;">{fl}</div>
    <div style="flex:1;min-width:0;">
      <div style="font-size:13px;font-weight:700;color:#E2E8F0;white-space:nowrap;
                  overflow:hidden;text-overflow:ellipsis;">{sel_est}</div>
      <div style="font-size:10px;color:#94A3B8;margin-bottom:3px;">{cr["Region"]} · {sel_est_yr}</div>
      <span style="background:#818CF822;color:#818CF8;border:1px solid #818CF833;
                   border-radius:4px;padding:2px 7px;font-size:8px;font-weight:600;">ESTIMATED</span>
    </div>
    <div style="text-align:right;">
      <div style="font-size:8px;color:#94A3B8;text-transform:uppercase;">Score</div>
      <div style="font-size:26px;font-weight:700;color:#818CF8;
                  font-family:'JetBrains Mono',monospace;">{sc:.3f}</div>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:5px;margin-bottom:13px;">
    <div style="background:#1E2A40;border-radius:4px;padding:7px;text-align:center;">
      <div style="font-size:7.5px;color:#94A3B8;text-transform:uppercase;">Tier</div>
      <div style="font-size:14px;font-weight:700;color:{tc2};font-family:'JetBrains Mono',monospace;">{t}</div>
    </div>
    <div style="background:#1E2A40;border-radius:4px;padding:7px;text-align:center;">
      <div style="font-size:7.5px;color:#94A3B8;text-transform:uppercase;">Risk</div>
      <div style="font-size:12px;font-weight:700;color:{rc2};">{ri}</div>
    </div>
    <div style="background:#1E2A40;border-radius:4px;padding:7px;text-align:center;">
      <div style="font-size:7.5px;color:#94A3B8;text-transform:uppercase;">Method</div>
      <div style="font-size:11px;font-weight:600;color:#818CF8;">ML Est.</div>
    </div>
  </div>
  <div style="font-size:8px;color:#94A3B8;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px;">DOMAIN SCORES</div>
  {dom_rows}
  <div style="margin-top:10px;padding-top:10px;border-top:1px solid #263354;
              font-size:9px;color:#94A3B8;line-height:1.5;">
    {sel_est} falls outside the core 100-country tracked set and has no directly reported
    indicators. Domain scores above are model-estimated from the same six-domain regression
    used for the 2030 forecasts, so confidence is lower than for tracked countries.
  </div>
</div>""", unsafe_allow_html=True)

    with rc:
        items2 = "".join(list_item(r, False) for _, r in bot10.iterrows())
        st.markdown(f"""
<div style="background:#192133;border:1px solid #263354;border-radius:8px;overflow:hidden;height:530px;">
  <div style="padding:9px 11px;background:#1E2A40;border-bottom:1px solid #263354;">
    <span style="font-size:10px;color:#F87171;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;">
      ⚠️ BOTTOM 10 — MOST FRAGILE ({sel_est_yr})</span>
  </div>
  <div style="overflow-y:auto;max-height:485px;">{items2}</div>
</div>""", unsafe_allow_html=True)



# ─────────────────────────────────────────────────────────────────────────────
# 10. PAGE 6 — FORECAST 2030
# ─────────────────────────────────────────────────────────────────────────────

def page_forecast_2030(D):
    ranking  = D["ranking"]
    forecast = D["forecast"]

    # Only countries in forecast (100 actual countries)
    fc_countries = sorted(forecast["Country Name"].dropna().unique().tolist())
    def_c = "Switzerland" if "Switzerland" in fc_countries else fc_countries[0]

    # Row 0: Selector — aligned to 3-column card grid below
    sc = st.columns([1, 1, 1])
    with sc[0]:
        sel_c = st.selectbox("🔍 Select Country for 2030 Forecast",
                             fc_countries,
                             index=fc_countries.index(def_c),
                             key="p6_country",
                             label_visibility="visible")

    fc_c  = forecast[forecast["Country Name"] == sel_c]
    rk_c  = ranking[ranking["Country Name"] == sel_c]

    if fc_c.empty or rk_c.empty:
        st.markdown(f'<div style="background:#192133;border:1px solid #263354;border-radius:8px;'
                    f'padding:40px;text-align:center;color:#94A3B8;margin-top:20px;">'
                    f'No forecast data for <b style="color:#E2E8F0;">{sel_c}</b></div>',
                    unsafe_allow_html=True)
        return

    rk_row    = rk_c.iloc[0]
    c_code    = str(rk_row["Country Code"])
    region    = str(rk_row["Region"])
    data_type = str(rk_row["Data_Type"])
    base_sc   = float(rk_row["Composite_Base"])
    opt_sc    = float(rk_row["Composite_Opt"])
    pess_sc   = float(rk_row["Composite_Pess"])
    g_rank    = int(rk_row["Global_Rank_2030"])
    flag      = get_flag(c_code)

    t_base  = assign_tier(base_sc)
    r_base  = assign_risk(base_sc)
    tc_base = tier_color(t_base)
    rc_base = risk_color(r_base)
    dt_badge = (badge("ACTUAL","#38BDF8") if data_type=="Actual" else badge("ESTIMATED","#818CF8"))

    # Confidence
    if data_type == "Actual":
        conf = "High"
    else:
        conf = "Low"
    cc2 = conf_color(conf)

    # Row 1: Three columns
    fc_col, sc_col2, rec_col = st.columns([4, 4, 4])

    # --- Forecast Card ---
    with fc_col:
        dom_rows_html = ""
        for dom in DOMAINS:
            dr = fc_c[fc_c["Domain"] == dom]
            ds = float(dr["Base_2030"].values[0]) if not dr.empty else 0.0
            dc = DOMAIN_COLORS.get(dom,"#94A3B8")
            dom_rows_html += (f'<div style="margin-bottom:10px;">'
                              f'<div style="display:flex;justify-content:space-between;margin-bottom:4px;">'
                              f'<span style="font-size:13px;color:#E2E8F0;">{DOMAIN_ICONS.get(dom,"")} {dom}</span>'
                              f'<span style="font-size:13px;color:{dc};font-family:\'JetBrains Mono\',monospace;">{ds:.3f}</span></div>'
                              f'{pbr(ds,dc,3)}</div>')

        st.markdown(f"""
<div style="background:#192133;border:1px solid #263354;border-top:4px solid #38BDF8;
            border-radius:8px;padding:18px;height:550px;overflow:hidden;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:15px;
              padding-bottom:12px;border-bottom:1px solid #263354;">
    <div style="font-size:36px;">{flag}</div>
    <div style="flex:1;min-width:0;">
      <div style="font-size:14px;font-weight:700;color:#E2E8F0;white-space:nowrap;
                  overflow:hidden;text-overflow:ellipsis;">{sel_c}</div>
      <div style="font-size:9px;color:#94A3B8;margin-bottom:3px;">{region}</div>
      {dt_badge}
    </div>
    <div style="text-align:right;flex-shrink:0;">
      <div style="font-size:8px;color:#94A3B8;text-transform:uppercase;letter-spacing:0.05em;">2030 Base</div>
      <div style="font-size:28px;font-weight:700;color:#38BDF8;
                  font-family:'JetBrains Mono',monospace;line-height:1.1;">{base_sc:.3f}</div>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:5px;margin-bottom:13px;">
    <div style="background:#1E2A40;border-radius:4px;padding:6px;text-align:center;">
      <div style="font-size:8px;color:#94A3B8;text-transform:uppercase;">Rank</div>
      <div style="font-size:14px;font-weight:700;color:#E2E8F0;
                  font-family:'JetBrains Mono',monospace;">#{g_rank}</div>
    </div>
    <div style="background:#1E2A40;border-radius:4px;padding:6px;text-align:center;">
      <div style="font-size:8px;color:#94A3B8;text-transform:uppercase;">Tier</div>
      <div style="font-size:14px;font-weight:700;color:{tc_base};
                  font-family:'JetBrains Mono',monospace;">{t_base}</div>
    </div>
    <div style="background:#1E2A40;border-radius:4px;padding:6px;text-align:center;">
      <div style="font-size:8px;color:#94A3B8;text-transform:uppercase;">Risk</div>
      <div style="font-size:12px;font-weight:700;color:{rc_base};">{r_base}</div>
    </div>
    <div style="background:#1E2A40;border-radius:4px;padding:6px;text-align:center;">
      <div style="font-size:8px;color:#94A3B8;text-transform:uppercase;">Conf.</div>
      <div style="font-size:12px;font-weight:700;color:{cc2};">{conf}</div>
    </div>
  </div>
  <div style="font-size:9px;color:#94A3B8;letter-spacing:0.08em;
              text-transform:uppercase;margin-bottom:9px;">DOMAIN FORECASTS (BASE 2030)</div>
  {dom_rows_html}
</div>""", unsafe_allow_html=True)

    # --- Scenario Comparison ---
    with sc_col2:
        scenarios = [
            ("🟢 Optimistic", opt_sc,  "#34D399", "Optimistic_2030"),
            ("🔵 Base",        base_sc, "#38BDF8", "Base_2030"),
            ("🔴 Pessimistic", pess_sc, "#F87171", "Pessimistic_2030"),
        ]
        all_base = ranking["Composite_Base"].sort_values(ascending=False).values

        scen_cards = ""
        for sname, sscore, scolor, _ in scenarios:
            st_val = assign_tier(sscore)
            sr_val = assign_risk(sscore)
            stc    = tier_color(st_val)
            src    = risk_color(sr_val)
            approx_rank = int(np.searchsorted(-all_base, -sscore)) + 1
            scen_cards += f"""
<div style="background:#1E2A40;border:1px solid #263354;border-left:3px solid {scolor};
            border-radius:6px;padding:16px 18px;margin-bottom:14px;">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
    <div style="font-size:13px;font-weight:700;color:{scolor};">{sname}</div>
    <div style="font-size:22px;font-weight:700;color:{scolor};
                font-family:'JetBrains Mono',monospace;">{sscore:.3f}</div>
  </div>
  <div style="display:flex;gap:14px;margin-bottom:8px;">
    <div><span style="font-size:8px;color:#94A3B8;">RANK </span>
         <span style="font-size:10.5px;color:#E2E8F0;font-family:'JetBrains Mono',monospace;">~#{approx_rank}</span></div>
    <div><span style="font-size:8px;color:#94A3B8;">TIER </span>
         <span style="font-size:10.5px;color:{stc};">{st_val}</span></div>
    <div><span style="font-size:8px;color:#94A3B8;">RISK </span>
         <span style="font-size:10.5px;color:{src};">{sr_val}</span></div>
  </div>
  {pbr(sscore,scolor,5)}
</div>"""

        spread = opt_sc - pess_sc
        sens_txt = "high sensitivity to policy decisions" if spread > 0.08 else "a relatively stable trajectory regardless of scenario"

        st.markdown(f"""
<div style="background:#192133;border:1px solid #263354;border-radius:8px;
            padding:18px;height:550px;overflow:hidden;">
  <div style="font-size9px;color:#94A3B8;font-weight:600;letter-spacing:0.1em;
              text-transform:uppercase;margin-bottom:13px;">📊 SCENARIO ANALYSIS — 2030</div>
  {scen_cards}
  <div style="margin-top:4px;padding-top:12px;border-top:1px solid #263354;
              font-size:10px;color:#94A3B8;line-height:1.6;">
    Optimistic–Pessimistic spread of
    <span style="color:#E2E8F0;font-family:'JetBrains Mono',monospace;">{spread:.3f}</span>
    points to <b style="color:#E2E8F0;">{sens_txt}</b>.
  </div>
</div>""", unsafe_allow_html=True)

    # --- Recommendation Panel ---
    with rec_col:
        best_dom_row  = fc_c.loc[fc_c["Base_2030"].idxmax()] if not fc_c.empty else None
        worst_dom_row = fc_c.loc[fc_c["Base_2030"].idxmin()] if not fc_c.empty else None
        spread = opt_sc - pess_sc

        if best_dom_row is not None:
            bd  = str(best_dom_row["Domain"])
            bs  = float(best_dom_row["Base_2030"])
            wd  = str(worst_dom_row["Domain"])
            ws  = float(worst_dom_row["Base_2030"])
            sens = "high sensitivity to policy decisions" if spread > 0.08 else "relatively stable trajectory"
            rec_s = (f'{sel_c}\'s strongest projected domain is '
                     f'{DOMAIN_ICONS.get(bd,"")} <b>{bd}</b> '
                     f'<span style="font-family:\'JetBrains Mono\',monospace;">(Base: {bs:.3f})</span>, '
                     f'indicating structural resilience capacity through 2030.')
            rec_i = (f'{DOMAIN_ICONS.get(wd,"")} <b>{wd}</b> '
                     f'<span style="font-family:\'JetBrains Mono\',monospace;">(Base: {ws:.3f})</span> '
                     f'is the critical gap. Targeted investment here could materially improve overall rank.')
            rec_a = (f'Scenario spread of '
                     f'<span style="font-family:\'JetBrains Mono\',monospace;">{spread:.3f}</span> '
                     f'indicates <b>{sens}</b>. Prioritize stabilizing lowest-scoring domains '
                     f'and leverage <b>{bd}</b> as a platform.')
            rec_o = (f'Under the base scenario, <b>{sel_c}</b> projects Tier <b>{t_base}</b> by 2030 '
                     f'at score <span style="font-family:\'JetBrains Mono\',monospace;color:#38BDF8;">{base_sc:.3f}</span> '
                     f'(Rank #{g_rank} globally), '
                     f'{"maintaining" if base_sc > 0.6 else "building toward"} a resilient standing in <b>{region}</b>.')
        else:
            rec_s = rec_i = rec_a = rec_o = "Insufficient data."

        st.markdown(f"""
<div style="background:#192133;border:1px solid #263354;border-radius:8px;
            padding:18px;height:550px;overflow:hidden;">
  <div style="font-size:13px;color:#94A3B8;font-weight:600;letter-spacing:0.1em;
              text-transform:uppercase;margin-bottom:14px;">📋 EXECUTIVE RECOMMENDATION</div>

  <div style="margin-bottom:18px;">
    <div style="font-size:10px;color:#34D399;font-weight:700;text-transform:uppercase;
                letter-spacing:0.08em;margin-bottom:6px;">✅ STRENGTHS</div>
    <div style="font-size:13px;color:#E2E8F0;line-height:1.7;">{rec_s}</div>
  </div>

  <div style="border-top:1px solid #263354;padding-top:16px;margin-bottom:18px;">
    <div style="font-size:10px;color:#FBBF24;font-weight:700;text-transform:uppercase;
                letter-spacing:0.08em;margin-bottom:6px;">⚠️ AREAS TO IMPROVE</div>
    <div style="font-size:13px;color:#E2E8F0;line-height:1.7;">{rec_i}</div>
  </div>

  <div style="border-top:1px solid #263354;padding-top:16px;margin-bottom:18px;">
    <div style="font-size:10px;color:#818CF8;font-weight:700;text-transform:uppercase;
                letter-spacing:0.08em;margin-bottom:6px;">🎯 PRIORITY ACTIONS</div>
    <div style="font-size:13px;color:#E2E8F0;line-height:1.7;">{rec_a}</div>
  </div>

  <div style="border-top:1px solid #263354;padding-top:16px;">
    <div style="background:#1E2A40;border-radius:6px;padding:14px 16px;">
      <div style="font-size:10px;color:#38BDF8;font-weight:700;text-transform:uppercase;
                  letter-spacing:0.08em;margin-bottom:6px;">📊 EXPECTED 2030 OUTCOME</div>
      <div style="font-size:13px;color:#E2E8F0;line-height:1.7;">{rec_o}</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 11. MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    inject_global_css()

    with st.spinner("Loading data…"):
        D = load_data()

    tabs = st.tabs([
        "🌐 Global Overview",
        "🧩 Domain Intelligence",
        "🔍 Country Explorer",
        "⚠️ Risk & Opportunity",
        "🔮 Estimated Explorer",
        "📡 Forecast 2030",
    ])

    with tabs[0]: page_global_overview(D)
    with tabs[1]: page_domain_intelligence(D)
    with tabs[2]: page_country_explorer(D)
    with tabs[3]: page_risk_opportunity(D)
    with tabs[4]: page_estimated_explorer(D)
    with tabs[5]: page_forecast_2030(D)


if __name__ == "__main__":
    main()

