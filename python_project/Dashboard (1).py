"""
Global Resilience Index — Streamlit Dashboard  v2
==================================================
6 pages · 100 countries · 6 domains · 2000–2023
"""

import os
import warnings
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# THEME PALETTE
# ─────────────────────────────────────────────────────────────────────────────
C = {
    "green":  "#2ecc71",
    "blue":   "#3498db",
    "gold":   "#f39c12",
    "red":    "#e74c3c",
    "purple": "#9b59b6",
    "teal":   "#1abc9c",
    "grey":   "#95a5a6",
    "bg":     "#0f1117",
    "card":   "#1a1d2e",
    "white":  "#ecf0f1",
}

REGION_COLORS = {
    "Europe":                       C["blue"],
    "North America":                C["teal"],
    "East Asia":                    C["purple"],
    "South America":                C["gold"],
    "Middle East":                  C["green"],
    "Central Asia":                 "#e67e22",
    "South Asia":                   "#c0392b",
    "Africa":                       C["red"],
    "Oceania":                      "#16a085",
    "Central America & Caribbean":  "#8e44ad",
}

TIER_COLORS = {
    "High Resilience": C["green"],
    "Medium-High":     C["blue"],
    "Medium-Low":      C["gold"],
    "Low Resilience":  C["red"],
}

DOMAIN_COLORS = {
    "Digital Infrastructure": C["blue"],
    "Economic Fragility":     C["red"],
    "Food Security":          C["gold"],
    "Healthcare":             C["green"],
    "Political Stability":    C["purple"],
    "Climate & Energy":       C["teal"],
}

def theme(fig, height=None):
    """Apply consistent dark theme to any plotly figure."""
    upd = dict(
        paper_bgcolor=C["bg"],
        plot_bgcolor=C["card"],
        font_color=C["white"],
        font_family="Inter, sans-serif",
        title_font_size=15,
        title_font_color=C["white"],
        legend=dict(bgcolor="rgba(0,0,0,0)", font_color=C["white"]),
        xaxis=dict(gridcolor="#2a2d3e", zerolinecolor="#2a2d3e"),
        yaxis=dict(gridcolor="#2a2d3e", zerolinecolor="#2a2d3e"),
        margin=dict(l=10, r=10, t=45, b=10),
    )
    if height:
        upd["height"] = height
    fig.update_layout(**upd)
    return fig


def kpi_card(col, label, value, delta=None, delta_color="normal", help_text=None):
    col.metric(label=label, value=value, delta=delta,
               delta_color=delta_color, help=help_text)


def insight_box(text: str, icon: str = "💡"):
    st.markdown(
        f"""<div style='background:{C["card"]};border-left:4px solid {C["blue"]};
        padding:12px 16px;border-radius:4px;margin:8px 0;font-size:14px;
        color:{C["white"]};line-height:1.6'>{icon}&nbsp;&nbsp;{text}</div>""",
        unsafe_allow_html=True,
    )


def section(title: str, subtitle: str = ""):
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Global Resilience Index",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
[data-testid="metric-container"] {
    background: #1a1d2e;
    border: 1px solid #2a2d3e;
    border-radius: 8px;
    padding: 12px 16px;
}
[data-testid="stMetricLabel"] { font-size: 12px !important; color: #95a5a6 !important; }
[data-testid="stMetricValue"] { font-size: 22px !important; font-weight: 700 !important; }
.stDataFrame { border-radius: 8px; }
.block-container { padding-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS (identical to notebook)
# ─────────────────────────────────────────────────────────────────────────────
COUNTRY_CODES = {
    'GEO','MDA','ESP','CHE','GBR','HUN','MYS','RUS','CAN','ISL','NZL','TUR','KOR','MUS','THA',
    'JOR','KAZ','BLR','PHL','KGZ','AUS','BWA','COL','ARM','USA','CHL','LKA','MEX','IND','TUN',
    'AZE','BIH','UKR','CRI','ALB','ARE','URY','JAM','BRA','SLV','NOR','PER','AUT','BEL','CHN',
    'DEU','ISR','LVA','CZE','EST','FRA','IRL','ITA','MLT','NLD','PRT','PAK','IDN','FIN','LTU',
    'ROU','SVK','SVN','SWE','MNG','HRV','PAN','DNK','ECU','GRC','OMN','POL','SGP','BGD','BHR',
    'CYP','MAR','MKD','EGY','LUX','MOZ','BOL','KWT','ZMB','SAU','NPL','BFA','NIC','VNM','GTM',
    'KHM','RWA','PRY','TJK','TGO','ETH','SWZ','GHA','NAM','MDG','DOM','UZB',
}
EXCLUDED_NAMES     = {'Egypt, Arab Rep.', 'Israel'}
EXCLUDED_YEARS     = {2024, 2025}
EXCLUDED_FAO_YEARS = {2024, 2025, 2026}

INVERSE_INDICATORS = {
    'FP.CPI.TOTL.ZG', 'NY.GDP.MKTP.KD.ZG',
    'TM.VAL.FOOD.ZS.UN', 'SN.ITK.DEFC.ZS', 'EG.USE.ELEC.KH.PC',
}

INDICATOR_DOMAIN = {
    'IT.NET.BBND.P2':       'Digital Infrastructure',
    'IT.NET.USER.ZS':       'Digital Infrastructure',
    'NY.GDP.MKTP.KD.ZG':    'Economic Fragility',
    'FP.CPI.TOTL.ZG':       'Economic Fragility',
    'TM.VAL.FOOD.ZS.UN':    'Food Security',
    'SN.ITK.DEFC.ZS':       'Food Security',
    'SH.XPD.CHEX.GD.ZS':   'Healthcare',
    'SH.MED.BEDS.ZS':       'Healthcare',
    'SH.MED.PHYS.ZS':       'Healthcare',
    'PV.EST':               'Political Stability',
    'EG.ELC.ACCS.ZS':       'Climate & Energy',
    'EG.CFT.ACCS.ZS':       'Climate & Energy',
    'EG.FEC.RNEW.ZS':       'Climate & Energy',
    'EG.USE.ELEC.KH.PC':    'Climate & Energy',
    'EN.GHG.CO2.PC.CE.AR5': 'Climate & Energy',
}

REGION_MAP = {
    **dict.fromkeys(['MAR','TUN','MOZ','ZMB','BWA','NAM','RWA','ETH','GHA','TGO','BFA','SWZ','MDG','MUS'], 'Africa'),
    **dict.fromkeys(['SAU','ARE','KWT','OMN','JOR','BHR'], 'Middle East'),
    **dict.fromkeys(['IND','PAK','BGD','LKA','NPL'], 'South Asia'),
    **dict.fromkeys(['CHN','IDN','MYS','THA','VNM','KHM','PHL','SGP','KOR','MNG'], 'East Asia'),
    **dict.fromkeys(['KAZ','UZB','KGZ','TJK','AZE','ARM','GEO'], 'Central Asia'),
    **dict.fromkeys([
        'DEU','FRA','ITA','ESP','PRT','NLD','BEL','AUT','CHE','LUX','IRL','GBR','NOR','SWE',
        'FIN','DNK','ISL','POL','CZE','SVK','HUN','ROU','GRC','EST','LVA','LTU','SVN','HRV',
        'BIH','MKD','ALB','UKR','BLR','MDA','RUS','MLT','CYP','TUR'], 'Europe'),
    **dict.fromkeys(['USA','CAN','MEX'], 'North America'),
    **dict.fromkeys(['BRA','COL','CHL','PER','URY','PRY','BOL','ECU'], 'South America'),
    **dict.fromkeys(['AUS','NZL'], 'Oceania'),
    **dict.fromkeys(['GTM','SLV','NIC','PAN','CRI','DOM','JAM'], 'Central America & Caribbean'),
}

FAO_COLUMNS = {
    'Food':    'Food Price Index',
    'Meat':    'Meat Price Index',
    'Dairy':   'Dairy Price Index',
    'Cereals': 'Cereals Price Index',
    'Oils':    'Oils Price Index',
    'Sugar':   'Sugar Price Index',
}

STD_COLS = ['Country Name', 'Country Code', 'Indicator Code', 'Indicator Name', 'Year', 'Value']

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def load_wb_file(path, label, year_col='Year'):
    if not os.path.exists(path):
        return pd.DataFrame(columns=STD_COLS)
    df = pd.read_excel(path)
    df.columns = [c.lstrip('\ufeff').strip() for c in df.columns]
    if year_col != 'Year' and year_col in df.columns:
        df = df.rename(columns={year_col: 'Year'})
    if 'Indicator Name' not in df.columns:
        df['Indicator Name'] = np.nan
    df['Year']  = pd.to_numeric(df['Year'],  errors='coerce').astype('Int64')
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    df = df[~df['Year'].isin(EXCLUDED_YEARS)]
    return df[STD_COLS].copy()

def load_fao_file(path):
    if not os.path.exists(path):
        return pd.DataFrame()
    df = pd.read_excel(path)
    df.columns = [c.lstrip('\ufeff').strip() for c in df.columns]
    df['Date']  = pd.to_datetime(df['Date'], errors='coerce')
    df['Year']  = df['Date'].dt.year.astype('Int64')
    df['Month'] = df['Date'].dt.month.astype('Int64')
    df = df[~df['Year'].isin(EXCLUDED_FAO_YEARS)]
    for col in FAO_COLUMNS.values():
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


def get_price_category(price):
    if price < 50:    return 'Extremely Cheap'
    elif price < 60:  return 'Very Cheap'
    elif price < 70:  return 'Cheap'
    elif price < 80:  return 'Slightly Cheap'
    elif price < 90:  return 'Below Normal'
    elif price < 100: return 'Near Normal'
    elif price < 110: return 'Slightly Expensive'
    elif price < 120: return 'Moderately Expensive'
    elif price < 140: return 'Expensive'
    else:             return 'Very Expensive'

# ─────────────────────────────────────────────────────────────────────────────
# DATA PIPELINE
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading source data…")
def build_data(data_dir: str):
    def p(sub, fn):
        return os.path.join(data_dir, sub, fn)

    df_broadband  = load_wb_file(p("Digital Infrastructure", "Fixed broadband subscriptions.xlsx"), "Broadband")
    df_internet   = load_wb_file(p("Digital Infrastructure", "Internet Users.xlsx"), "Internet")
    df_gdp        = load_wb_file(p("Economic Fragility", "GDP Growth.xlsx"), "GDP")
    df_inflation  = load_wb_file(p("Economic Fragility", "Inflation.xlsx"), "Inflation")
    df_govt_debt  = load_wb_file(p("Economic Fragility", "Government Debt.xlsx"), "Govt Debt")
    df_food_imp   = load_wb_file(p("Food", "Food Imports _ of merchandise imports.xlsx"), "Food Imports")
    df_undernour  = load_wb_file(p("Food", "Prevalence of Undernourishment.xlsx"), "Undernourishment")
    df_fao_raw    = load_fao_file(p("Food", "FAO Food Price Index.xlsx"))
    df_health_exp = load_wb_file(p("Healthcare Capacity", "Global Health Expenditure.xlsx"), "Health Exp")
    df_hospitals  = load_wb_file(p("Healthcare Capacity", "Hospitals.xlsx"), "Hospitals", year_col="Attribute")
    df_physicians = load_wb_file(p("Healthcare Capacity", "Physicians.xlsx"), "Physicians")
    df_pol_stab   = load_wb_file(p("Political Stability", "Political Stability.xlsx"), "Pol Stability")
    df_elec_acc   = load_wb_file(p("Climate & Energy", "Access to electricity.xlsx"), "Elec Access")
    df_clean_fuel = load_wb_file(p("Climate & Energy", "Clean Fuel Access.xlsx"), "Clean Fuel")
    df_co2        = load_wb_file(p("Climate & Energy", "CO2 emissions  .xlsx"), "CO2")
    df_elec_cons  = load_wb_file(p("Climate & Energy", "Electricity consumption  .xlsx"), "Elec Cons")
    df_renewable  = load_wb_file(p("Climate & Energy", "Renewable energy  .xlsx"), "Renewable")

    all_dfs = [
        df_broadband, df_internet, df_gdp, df_inflation,
        df_food_imp, df_undernour, df_health_exp, df_hospitals,
        df_physicians, df_pol_stab, df_elec_acc, df_clean_fuel,
        df_co2, df_elec_cons, df_renewable,
    ]
    all_data = pd.concat(all_dfs, ignore_index=True)

    country_list = (all_data[['Country Name', 'Country Code']].drop_duplicates()
                    .dropna(subset=['Country Code']))
    country_list = country_list[country_list['Country Code'].isin(COUNTRY_CODES)]
    country_list = country_list[~country_list['Country Name'].isin(EXCLUDED_NAMES)]
    country_list = country_list.sort_values('Country Code').reset_index(drop=True)
    country_list['Region'] = country_list['Country Code'].map(REGION_MAP).fillna('Other')
    country_list.insert(0, 'Country_Key', range(1, len(country_list) + 1))

    indicator_list = (all_data[['Indicator Code', 'Indicator Name']]
                      .drop_duplicates(subset='Indicator Code')
                      .dropna(subset=['Indicator Code'])
                      .sort_values('Indicator Code').reset_index(drop=True))
    indicator_list['Domain'] = indicator_list['Indicator Code'].map(INDICATOR_DOMAIN).fillna('Other')
    indicator_list.insert(0, 'Indicator_Key', range(1, len(indicator_list) + 1))

    year_list = [y for y in sorted(all_data['Year'].dropna().astype(int).unique())
                 if y not in EXCLUDED_YEARS]
    dim_year  = pd.DataFrame({'Year': year_list})
    dim_year['Decade'] = (dim_year['Year'] // 10 * 10).astype(str) + 's'

    raw = pd.concat([df[STD_COLS] for df in all_dfs], ignore_index=True)
    raw = raw.dropna(subset=['Year', 'Value'])
    raw['Year']  = raw['Year'].astype(int)
    raw['Value'] = pd.to_numeric(raw['Value'], errors='coerce')
    raw = raw.dropna(subset=['Value'])
    valid_countries = set(country_list['Country Code'])
    raw = raw[raw['Country Code'].isin(valid_countries)].copy()

    minmax = raw.groupby('Indicator Code')['Value'].agg(min_val='min', max_val='max').reset_index()

    fct = raw.copy()
    fct = fct.merge(country_list[['Country Code', 'Country Name', 'Region', 'Country_Key']],
                    on='Country Code', how='inner', suffixes=('', '_dup'))
    if 'Country Name_dup' in fct.columns:
        fct.drop(columns=['Country Name_dup'], inplace=True)
    fct = fct.merge(indicator_list[['Indicator Code', 'Domain', 'Indicator_Key']],
                    on='Indicator Code', how='inner')
    dim_year['Year_int'] = dim_year['Year'].astype(int)
    fct = fct.merge(dim_year[['Year_int', 'Decade']].rename(columns={'Year_int': 'Year'}),
                    on='Year', how='inner')
    fct = fct.merge(minmax, on='Indicator Code', how='left')

    fct['norm_raw'] = np.where(
        (fct['max_val'] == fct['min_val']) | fct['max_val'].isna() | fct['min_val'].isna(),
        0.5,
        0.01 + ((fct['Value'] - fct['min_val']) / (fct['max_val'] - fct['min_val'])) * 0.99,
    )
    fct['Normalized Value'] = np.where(
        fct['Indicator Code'].isin(INVERSE_INDICATORS),
        1 - fct['norm_raw'], fct['norm_raw'],
    ).clip(0.0, 1.0)

    # FAO food price index
    fao_parts = []
    for commodity, col_name in FAO_COLUMNS.items():
        if df_fao_raw.empty or col_name not in df_fao_raw.columns:
            continue
        tmp = df_fao_raw[['Month', 'Year', col_name]].copy()
        tmp = tmp.rename(columns={col_name: 'Price Index'})
        tmp['Type'] = commodity
        fao_parts.append(tmp)

    if fao_parts:
        fi = pd.concat(fao_parts, ignore_index=True)
        fi['Price Index'] = pd.to_numeric(fi['Price Index'], errors='coerce')
        fi = fi.dropna(subset=['Price Index'])
        fi['Price Category'] = fi['Price Index'].apply(get_price_category)
        fi['Year'] = fi['Year'].astype(int)
        fi = fi.merge(dim_year[['Year_int', 'Decade']].rename(columns={'Year_int': 'Year'}),
                      on='Year', how='left')
    else:
        fi = pd.DataFrame(columns=['Month', 'Year', 'Price Index', 'Type', 'Price Category', 'Decade'])

    govt_clean = df_govt_debt.dropna(subset=['Year']).copy()
    govt_clean['Year'] = govt_clean['Year'].astype(int)
    govt_clean = govt_clean[~govt_clean['Year'].isin(EXCLUDED_YEARS)]

    return fct, fi, country_list, indicator_list, dim_year, govt_clean, valid_countries


# ─────────────────────────────────────────────────────────────────────────────
# ANALYTICAL TABLES  (same logic as notebook)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Computing analytical tables…")
def build_tables(_fct, _fi, _govt_clean, _valid_countries):
    fct            = _fct
    fi             = _fi
    govt_clean     = _govt_clean
    valid_countries = _valid_countries

    # A1 – country ranking
    A1 = (fct.groupby(['Country Name', 'Region'])['Normalized Value']
          .mean().round(4).reset_index()
          .rename(columns={'Normalized Value': 'Composite Resilience Score'})
          .sort_values('Composite Resilience Score', ascending=False)
          .reset_index(drop=True))
    A1.insert(0, 'Rank', range(1, len(A1) + 1))

    domain_avgs = fct.groupby('Domain')['Normalized Value'].mean()

    # A3 – global domain averages
    A3 = (domain_avgs.round(4).reset_index()
          .rename(columns={'Normalized Value': 'Global Domain Average'})
          .sort_values('Global Domain Average', ascending=False))

    # A4 – region × domain matrix
    A4 = (fct.groupby(['Region', 'Domain'])['Normalized Value'].mean().round(4).reset_index()
          .rename(columns={'Normalized Value': 'Avg Resilience Score'})
          .sort_values(['Region', 'Domain']))

    # A5 – yearly trend
    A5 = (fct.groupby(['Year', 'Decade'])['Normalized Value'].mean().round(4).reset_index()
          .rename(columns={'Normalized Value': 'Avg Resilience'}).sort_values('Year'))

    # A6 – decade trend
    A6 = (fct.groupby('Decade')['Normalized Value'].mean().round(4).reset_index()
          .rename(columns={'Normalized Value': 'Avg Resilience'}).sort_values('Decade'))

    # A7 – domain pivot per country
    A7 = (fct.groupby(['Country Name', 'Region', 'Domain'])['Normalized Value']
          .mean().round(4).unstack('Domain').reset_index())
    A7.columns.name = None
    composite = (fct.groupby(['Country Name', 'Region'])['Normalized Value']
                 .mean().round(4).reset_index()
                 .rename(columns={'Normalized Value': 'Composite Score'}))
    A7 = A7.merge(composite, on=['Country Name', 'Region']).sort_values('Composite Score', ascending=False)

    # A8 – high risk countries
    base_scores = (fct.groupby(['Country Name', 'Region'])['Normalized Value']
                   .mean().round(4).reset_index()
                   .rename(columns={'Normalized Value': 'Composite Score'}))
    A8 = base_scores[base_scores['Composite Score'] < 0.5].copy()
    A8['Risk Category'] = 'High Risk'
    A8 = A8.sort_values('Composite Score')

    # A9 – stable countries
    A9 = base_scores[base_scores['Composite Score'] >= 0.5].copy()
    A9['Risk Category'] = 'Stable'
    A9 = A9.sort_values('Composite Score', ascending=False)

    # A10 – food price trend
    A10 = (fi.groupby(['Year', 'Type', 'Price Category'])['Price Index']
           .agg(Avg='mean', Max='max', Min='min').round(2).reset_index()
           .sort_values(['Year', 'Type']))

    # A13 – decade improvement
    decade_scores = (fct.groupby(['Country Name', 'Region', 'Decade'])['Normalized Value']
                     .mean().round(4).unstack('Decade'))
    decade_scores.columns.name = None
    decade_scores = decade_scores.reset_index()
    avail = [c for c in ['2000s', '2010s', '2020s'] if c in decade_scores.columns]
    A13 = decade_scores[['Country Name', 'Region'] + avail].copy()
    if '2000s' in A13.columns and '2020s' in A13.columns:
        A13['Decade_Improvement'] = (A13['2020s'] - A13['2000s']).round(4)
    A13 = A13.sort_values('Decade_Improvement', ascending=False)

    # A15 – political stability trend
    A15 = (fct[fct['Indicator Code'] == 'PV.EST']
           .groupby('Year')['Value'].mean().round(4).reset_index()
           .rename(columns={'Value': 'Avg Political Stability Index'}).sort_values('Year'))

    A16 = A1.head(10).copy()
    A17 = A1.tail(10).sort_values('Composite Resilience Score').copy()

    # A18 – region ranking
    A18 = (fct.groupby('Region').agg(
               Region_Resilience_Score=('Normalized Value', 'mean'),
               Country_Count=('Country Name', 'nunique'))
           .round(4).reset_index()
           .sort_values('Region_Resilience_Score', ascending=False)
           .reset_index(drop=True))
    A18.insert(0, 'Rank', range(1, len(A18) + 1))

    # A20 – resilience tiers
    A20 = A1.copy()
    A20['Resilience Tier'] = pd.cut(
        A20['Composite Resilience Score'],
        bins=[-np.inf, 0.40, 0.55, 0.70, np.inf],
        labels=['Low Resilience', 'Medium-Low', 'Medium-High', 'High Resilience'],
    )

    # A22 – double exposure
    health_avg = (fct[fct['Domain'] == 'Healthcare']
                  .groupby(['Country Name', 'Region'])['Normalized Value'].mean())
    food_raw   = (fct[fct['Indicator Code'] == 'SN.ITK.DEFC.ZS']
                  .groupby('Country Name')['Value'].mean())
    A22 = (health_avg.reset_index().rename(columns={'Normalized Value': 'Healthcare Score'})
           .merge(food_raw.reset_index().rename(columns={'Value': 'Avg Undernourishment %'}),
                  on='Country Name'))
    A22['Exposure Type'] = np.where(
        (A22['Healthcare Score'] < 0.4) & (A22['Avg Undernourishment %'] > 10),
        'Double Risk', 'Single / No Risk',
    )
    A22 = A22.round(4).sort_values(['Healthcare Score', 'Avg Undernourishment %'],
                                   ascending=[True, False])

    # A24 – GDP shocks
    A24 = (fct[fct['Indicator Code'] == 'NY.GDP.MKTP.KD.ZG']
           .groupby('Year')['Value'].agg(Avg='mean', Min='min', Max='max')
           .round(4).reset_index().sort_values('Year'))

    # A25 – 2022 food price shock
    fao_2020 = fi[fi['Year'] == 2020].groupby('Type')['Price Index'].mean()
    fao_2022 = fi[fi['Year'] == 2022].groupby('Type')['Price Index'].mean()
    A25 = pd.DataFrame({'Avg_2020': fao_2020, 'Avg_2022': fao_2022}).reset_index()
    if not A25.empty:
        A25['Pct_Change_vs_2020'] = (
            (A25['Avg_2022'] - A25['Avg_2020']) / A25['Avg_2020'] * 100).round(1)
        A25 = A25.sort_values('Pct_Change_vs_2020', ascending=False)

    # A33 – politically unstable countries
    A33 = (fct[fct['Indicator Code'] == 'PV.EST']
           .groupby(['Country Name', 'Region'])
           .agg(Avg_Pol_Stability=('Value', 'mean'),
                Normalized_Stability=('Normalized Value', 'mean'))
           .round(4).reset_index())
    A33 = A33[A33['Avg_Pol_Stability'] < -0.5].sort_values('Avg_Pol_Stability')

    # A36 – full risk sheet
    risk_base = (fct.groupby(['Country Name', 'Region'])
                 .agg(Composite_raw=('Normalized Value', 'mean')).reset_index())
    dom_wide  = (fct.groupby(['Country Name', 'Region', 'Domain'])['Normalized Value']
                 .mean().unstack('Domain').reset_index())
    dom_wide.columns.name = None
    energy_raw = (fct[fct['Indicator Code'] == 'EG.USE.ELEC.KH.PC']
                  .groupby(['Country Name', 'Region'])['Value'].mean().reset_index()
                  .rename(columns={'Value': 'Energy Score (kWh)'}))
    pol_raw = (fct[fct['Domain'] == 'Political Stability']
               .groupby(['Country Name', 'Region'])['Value'].mean().reset_index()
               .rename(columns={'Value': 'Political Stability Score'}))
    A36 = (risk_base.merge(dom_wide,    on=['Country Name', 'Region'], how='left')
                    .merge(energy_raw,  on=['Country Name', 'Region'], how='left')
                    .merge(pol_raw,     on=['Country Name', 'Region'], how='left'))
    A36['Composite Score'] = (A36['Composite_raw'] * 100).round(1)
    if 'Digital Infrastructure' in A36.columns:
        A36['Digital Score']            = (A36['Digital Infrastructure'] * 100).round(2)
    if 'Healthcare'             in A36.columns:
        A36['Health Score']             = (A36['Healthcare'] * 10).round(2)
    if 'Climate & Energy'       in A36.columns:
        A36['Climate Score']            = (A36['Climate & Energy'] * 100).round(2)
    if 'Economic Fragility'     in A36.columns:
        A36['Economic Fragility Score'] = (A36['Economic Fragility'] * 10).round(2)
    A36 = A36.sort_values('Composite Score', ascending=False).reset_index(drop=True)
    A36.insert(0, 'Rank', range(1, len(A36) + 1))
    keep_cols = [c for c in [
        'Rank', 'Country Name', 'Region', 'Composite Score', 'Digital Score',
        'Health Score', 'Energy Score (kWh)', 'Climate Score',
        'Political Stability Score', 'Economic Fragility Score',
    ] if c in A36.columns]
    A36 = A36[keep_cols]

    # ── KPIs ────────────────────────────────────────────────────────────────
    country_avg = fct.groupby('Country Name')['Normalized Value'].mean()
    region_avgs = fct.groupby('Region')['Normalized Value'].mean()

    # Most-improved region (2000s → 2020s)
    reg_decade = (fct.groupby(['Region', 'Decade'])['Normalized Value']
                  .mean().unstack('Decade'))
    reg_decade.columns.name = None
    if '2000s' in reg_decade.columns and '2020s' in reg_decade.columns:
        reg_decade['improvement'] = reg_decade['2020s'] - reg_decade['2000s']
        fastest_improving_region = reg_decade['improvement'].idxmax()
    else:
        fastest_improving_region = 'N/A'

    # Most-improved country
    if 'Decade_Improvement' in A13.columns:
        most_improved_country = A13.dropna(subset=['Decade_Improvement']).iloc[0]['Country Name']
    else:
        most_improved_country = 'N/A'

    fragile_country = A1.iloc[-1]['Country Name']

    kpis = {
        'avg_resilience':         round(fct['Normalized Value'].mean(), 4),
        'avg_risk':               round(fct[fct['Domain'].isin(['Economic Fragility', 'Political Stability'])]['Normalized Value'].mean(), 4),
        'food_dependency':        round(fct[fct['Indicator Code'] == 'TM.VAL.FOOD.ZS.UN']['Value'].mean(), 4),
        'food_vulnerability':     round(fct[fct['Domain'] == 'Food Security']['Normalized Value'].mean(), 4),
        'highest_survival':       round(country_avg.max(), 4),
        'most_resilient':         country_avg.idxmax(),
        'most_fragile':           fragile_country,
        'high_risk_count':        int((country_avg < 0.5).sum()),
        'stable_count':           int((country_avg >= 0.5).sum()),
        'strongest_domain':       domain_avgs.idxmax(),
        'weakest_domain':         domain_avgs.idxmin(),
        'top_region':             region_avgs.idxmax(),
        'lowest_region':          region_avgs.idxmin(),
        'fastest_improving_region': fastest_improving_region,
        'most_improved_country':  most_improved_country,
        'undernourishment':       round(fct[fct['Indicator Code'] == 'SN.ITK.DEFC.ZS']['Value'].mean(), 4),
        'total_countries':        int(fct['Country Name'].nunique()),
        'year_range':             f"{int(fct['Year'].min())}–{int(fct['Year'].max())}",
    }

    return (A1, A3, A4, A5, A6, A7, A8, A9, A10,
            A13, A15, A16, A17, A18, A20, A22, A24, A25, A33, A36, kpis)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌍 Global Resilience\n### Index Dashboard")
    st.caption("World Bank · 100 Countries · 2000–2023")
    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🌐 Overview",
            "🔍 Country Explorer",
            "🗺️ Regional Analysis",
            "⚠️ Risk & Stability",
            "🌾 Food Security",
            "⚡ Future Shock Index",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.caption("Data Source")
    data_dir = st.text_input(
        "Path to Final_Data_EXCEL folder",
        value=r"C:\Users\ASUS\Documents\Depi\Final_Data_EXCEL",
        help="Folder containing Digital Infrastructure, Economic Fragility, Food, etc.",
        label_visibility="collapsed",
    )
    load_btn = st.button("⟳  Load / Reload Data", type="primary", use_container_width=True)
    st.markdown("---")
    st.caption("Global Resilience Index v2 · Anthropic")

# ─────────────────────────────────────────────────────────────────────────────
# LOAD & CACHE
# ─────────────────────────────────────────────────────────────────────────────
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

if load_btn or not st.session_state.data_loaded:
    try:
        (fct, fi, country_list, indicator_list,
         dim_year, govt_clean, valid_countries) = build_data(data_dir)

        tables = build_tables(fct, fi, govt_clean, valid_countries)
        (A1, A3, A4, A5, A6, A7, A8, A9, A10,
         A13, A15, A16, A17, A18, A20, A22, A24, A25, A33, A36, kpis) = tables

        st.session_state.update({
            "data_loaded": True,
            "fct": fct, "fi": fi, "country_list": country_list,
            "A1": A1, "A3": A3, "A4": A4, "A5": A5, "A6": A6,
            "A7": A7, "A8": A8, "A9": A9, "A10": A10, "A13": A13,
            "A15": A15, "A16": A16, "A17": A17, "A18": A18, "A20": A20,
            "A22": A22, "A24": A24, "A25": A25, "A33": A33, "A36": A36,
            "kpis": kpis,
        })
    except Exception as exc:
        st.error(f"❌ Failed to load data: {exc}")
        st.stop()

if not st.session_state.data_loaded:
    st.info("👈 Set your data folder path in the sidebar and click **Load / Reload Data**.")
    st.stop()

# Pull from session
fct          = st.session_state["fct"]
fi           = st.session_state["fi"]
country_list = st.session_state["country_list"]
A1  = st.session_state["A1"];  A3  = st.session_state["A3"]
A4  = st.session_state["A4"];  A5  = st.session_state["A5"]
A6  = st.session_state["A6"];  A7  = st.session_state["A7"]
A8  = st.session_state["A8"];  A9  = st.session_state["A9"]
A10 = st.session_state["A10"]; A13 = st.session_state["A13"]
A15 = st.session_state["A15"]; A16 = st.session_state["A16"]
A17 = st.session_state["A17"]; A18 = st.session_state["A18"]
A20 = st.session_state["A20"]; A22 = st.session_state["A22"]
A24 = st.session_state["A24"]; A25 = st.session_state["A25"]
A33 = st.session_state["A33"]; A36 = st.session_state["A36"]
kpis = st.session_state["kpis"]


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ═════════════════════════════════════════════════════════════════════════════
if page == "🌐 Overview":
    st.title("🌐 Global Resilience Index")
    st.caption(f"World Bank Data Analysis · {kpis['total_countries']} Countries · 6 Domains · {kpis['year_range']}")

    # ── Executive Summary ────────────────────────────────────────────────────
    st.markdown("#### Executive Summary")

    top_score  = kpis['highest_survival']
    bot_score  = A1.iloc[-1]['Composite Resilience Score']
    decade_imp = A6.sort_values('Avg Resilience').iloc[-1]['Avg Resilience'] - A6.sort_values('Avg Resilience').iloc[0]['Avg Resilience']

    insight_box(
        f"<b>{kpis['most_resilient']}</b> leads the 100-country study with a composite score of "
        f"<b>{top_score:.3f}/1.0</b>, driven by strong performance in {kpis['strongest_domain']}. "
        f"<b>{kpis['most_fragile']}</b> ranks last at <b>{bot_score:.3f}</b>.",
        "🏆"
    )
    insight_box(
        f"<b>{kpis['top_region']}</b> is the most resilient region globally. "
        f"<b>{kpis['lowest_region']}</b> faces the most systemic challenges. "
        f"<b>{kpis['fastest_improving_region']}</b> posted the fastest improvement from the 2000s to the 2020s.",
        "🗺️"
    )
    insight_box(
        f"The weakest global domain is <b>{kpis['weakest_domain']}</b> — indicating this is the "
        f"single biggest driver of fragility across all 100 countries. "
        f"<b>{kpis['high_risk_count']}</b> countries score below the 0.5 risk threshold; "
        f"<b>{kpis['stable_count']}</b> are considered stable.",
        "⚠️"
    )
    insight_box(
        f"Global resilience improved by <b>+{decade_imp:.3f}</b> between the 2000s and 2020s. "
        f"<b>{kpis['most_improved_country']}</b> posted the largest single-country improvement over this period.",
        "📈"
    )

    st.markdown("---")

    # ── KPI Row ──────────────────────────────────────────────────────────────
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    kpi_card(k1, "Avg Resilience Score",   f"{kpis['avg_resilience']:.4f}")
    kpi_card(k2, "Avg Risk Score",          f"{kpis['avg_risk']:.4f}")
    kpi_card(k3, "Stable Countries",         str(kpis['stable_count']),
             delta=f"{kpis['stable_count']} / {kpis['total_countries']}")
    kpi_card(k4, "High-Risk Countries",      str(kpis['high_risk_count']),
             delta=f"score < 0.5", delta_color="inverse")
    kpi_card(k5, "Strongest Domain",         kpis['strongest_domain'])
    kpi_card(k6, "Weakest Domain",           kpis['weakest_domain'])

    st.markdown("---")

    # ── Yearly Resilience Trend ───────────────────────────────────────────────
    section("Global Resilience Trend (2000–2023)",
            "Average composite normalized score across all 100 countries and 15 indicators.")

    fig_trend = px.line(
        A5, x='Year', y='Avg Resilience', color='Decade',
        markers=True,
        color_discrete_sequence=[C["blue"], C["gold"], C["green"]],
    )
    fig_trend.add_hline(y=0.5, line_dash="dash", line_color=C["red"],
                        annotation_text="Risk Threshold  0.50",
                        annotation_font_color=C["red"])
    fig_trend.update_layout(
        yaxis_range=[0.35, 0.80],
        xaxis_title="Year", yaxis_title="Avg Normalized Score",
        legend_title="Decade",
    )
    theme(fig_trend, height=340)
    st.plotly_chart(fig_trend, use_container_width=True)

    # ── Domain + Tier row ────────────────────────────────────────────────────
    c1, c2 = st.columns([3, 2])

    with c1:
        section("Resilience by Domain",
                "Global average score across all countries per domain — higher = more resilient.")
        a3s = A3.sort_values('Global Domain Average')
        bar_colors = [DOMAIN_COLORS.get(d, C["blue"]) for d in a3s['Domain']]
        fig_dom = go.Figure(go.Bar(
            x=a3s['Global Domain Average'], y=a3s['Domain'],
            orientation='h',
            marker_color=bar_colors,
            text=a3s['Global Domain Average'].map('{:.4f}'.format),
            textposition='outside',
        ))
        fig_dom.add_vline(x=0.5, line_dash="dash", line_color=C["gold"],
                          annotation_text="0.50", annotation_font_color=C["gold"])
        fig_dom.update_layout(xaxis_range=[0, 0.95], xaxis_title="Avg Normalized Score",
                              yaxis_title="")
        theme(fig_dom, height=300)
        st.plotly_chart(fig_dom, use_container_width=True)

    with c2:
        section("Countries by Resilience Tier")
        tier_order  = ['High Resilience', 'Medium-High', 'Medium-Low', 'Low Resilience']
        tier_counts = (A20['Resilience Tier'].astype(str)
                       .value_counts().reindex(tier_order, fill_value=0)
                       .reset_index())
        tier_counts.columns = ['Tier', 'Count']
        fig_tier = go.Figure(go.Pie(
            labels=tier_counts['Tier'], values=tier_counts['Count'],
            hole=0.55,
            marker_colors=[TIER_COLORS[t] for t in tier_counts['Tier']],
            textinfo='label+percent',
            sort=False,
        ))
        fig_tier.update_layout(showlegend=False)
        theme(fig_tier, height=300)
        st.plotly_chart(fig_tier, use_container_width=True)

    # ── Decade bar ────────────────────────────────────────────────────────────
    section("Average Resilience by Decade",
            "Steady improvement from 2000s through 2020s.")
    fig_dec = go.Figure(go.Bar(
        x=A6['Decade'], y=A6['Avg Resilience'],
        marker_color=[C["blue"], C["teal"], C["green"]],
        text=A6['Avg Resilience'].map('{:.4f}'.format),
        textposition='outside',
    ))
    fig_dec.update_layout(yaxis_range=[0, A6['Avg Resilience'].max() + 0.06],
                          xaxis_title="Decade", yaxis_title="Avg Resilience Score")
    theme(fig_dec, height=260)
    st.plotly_chart(fig_dec, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 2 — COUNTRY EXPLORER
# ═════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Country Explorer":
    st.title("🔍 Country Explorer")
    st.caption("Drill into any country's resilience profile, domain scores, trend, and peer benchmarks.")

    # ── Filters ──────────────────────────────────────────────────────────────
    fc1, fc2, fc3 = st.columns(3)
    sel_region = fc1.selectbox("Filter by Region",
                               ["All"] + sorted(A1['Region'].unique().tolist()))
    tier_order_ui = ['All', 'High Resilience', 'Medium-High', 'Medium-Low', 'Low Resilience']
    sel_tier   = fc2.selectbox("Filter by Resilience Tier", tier_order_ui)
    all_countries_list = sorted(A7['Country Name'].unique().tolist())
    sel_country = fc3.selectbox("Country Spotlight", all_countries_list, index=0)

    # Filtered ranking table
    filtered = A20.copy()
    if sel_region != "All":
        filtered = filtered[filtered['Region'] == sel_region]
    if sel_tier != "All":
        filtered = filtered[filtered['Resilience Tier'].astype(str) == sel_tier]

    # ── Country Scorecard ─────────────────────────────────────────────────────
    st.markdown("---")
    section(f"📋 Country Scorecard — {sel_country}")

    c_row    = A1[A1['Country Name'] == sel_country].iloc[0]
    c_tier   = A20[A20['Country Name'] == sel_country]['Resilience Tier'].values[0]
    c_rank   = int(c_row['Rank'])
    c_score  = c_row['Composite Resilience Score']
    c_region = c_row['Region']

    sc1, sc2, sc3, sc4 = st.columns(4)
    kpi_card(sc1, "Overall Score",  f"{c_score:.4f}")
    kpi_card(sc2, "Global Rank",    f"#{c_rank} / {kpis['total_countries']}")
    kpi_card(sc3, "Region",          c_region)
    kpi_card(sc4, "Resilience Tier", str(c_tier))

    # Domain scores for scorecard
    domains_list = ['Digital Infrastructure', 'Economic Fragility', 'Food Security',
                    'Healthcare', 'Political Stability', 'Climate & Energy']
    c_a7 = A7[A7['Country Name'] == sel_country]
    if not c_a7.empty:
        d_scores = {d: float(c_a7[d].values[0]) if d in c_a7.columns and not pd.isna(c_a7[d].values[0]) else None
                    for d in domains_list}
        d_cols = st.columns(6)
        for col, (dom, val) in zip(d_cols, d_scores.items()):
            short = dom.replace(" Infrastructure", "").replace(" Fragility", "").replace(" Security", "").replace(" & Energy", "")
            if val is not None:
                col.metric(short, f"{val:.3f}")
            else:
                col.metric(short, "N/A")

    st.markdown("---")

    # ── Radar + Country Trend ─────────────────────────────────────────────────
    r1, r2 = st.columns(2)

    with r1:
        section("Domain Radar")
        if not c_a7.empty:
            # Replace NaN with 0 for radar — they're missing data, not zero score
            vals = [max(0.0, float(c_a7[d].values[0])) if d in c_a7.columns and not pd.isna(c_a7[d].values[0]) else 0.0
                    for d in domains_list]
            # Global averages for reference ring
            global_vals = [float(A3[A3['Domain'] == d]['Global Domain Average'].values[0])
                           if len(A3[A3['Domain'] == d]) > 0 else 0.5 for d in domains_list]

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=global_vals + [global_vals[0]],
                theta=domains_list + [domains_list[0]],
                fill='toself', fillcolor='rgba(149,165,166,0.12)',
                line=dict(color=C["grey"], dash='dash', width=1),
                name='Global Average',
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=domains_list + [domains_list[0]],
                fill='toself', fillcolor='rgba(52,152,219,0.20)',
                line=dict(color=C["blue"], width=2),
                name=sel_country,
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1],
                                           gridcolor="#2a2d3e", tickfont=dict(color=C["grey"]))),
                showlegend=True,
                legend=dict(orientation='h', y=-0.15),
            )
            theme(fig_radar, height=360)
            st.plotly_chart(fig_radar, use_container_width=True)

    with r2:
        section("Resilience Trend over Time")
        c_trend = (fct[fct['Country Name'] == sel_country]
                   .groupby('Year')['Normalized Value'].mean().round(4).reset_index()
                   .rename(columns={'Normalized Value': 'Avg Resilience'}))

        # Global average for benchmark
        global_trend = A5[['Year', 'Avg Resilience']].rename(columns={'Avg Resilience': 'Global Avg'})
        # Regional average
        c_reg = c_region
        reg_trend = (fct[fct['Region'] == c_reg]
                     .groupby('Year')['Normalized Value'].mean().round(4).reset_index()
                     .rename(columns={'Normalized Value': 'Regional Avg'}))

        fig_trend2 = go.Figure()
        fig_trend2.add_scatter(x=global_trend['Year'], y=global_trend['Global Avg'],
                               mode='lines', name='Global Average',
                               line=dict(color=C["grey"], dash='dot', width=1))
        fig_trend2.add_scatter(x=reg_trend['Year'], y=reg_trend['Regional Avg'],
                               mode='lines', name=f'{c_reg} Avg',
                               line=dict(color=C["gold"], dash='dash', width=1.5))
        fig_trend2.add_scatter(x=c_trend['Year'], y=c_trend['Avg Resilience'],
                               mode='lines+markers', name=sel_country,
                               line=dict(color=C["blue"], width=2.5),
                               marker=dict(size=5))
        fig_trend2.add_hline(y=0.5, line_dash="dash", line_color=C["red"],
                             annotation_text="Risk 0.50", annotation_font_color=C["red"])
        fig_trend2.update_layout(xaxis_title="Year", yaxis_title="Avg Normalized Score",
                                 legend=dict(orientation='h', y=-0.2),
                                 yaxis_range=[0, 1.0])
        theme(fig_trend2, height=360)
        st.plotly_chart(fig_trend2, use_container_width=True)

    # ── Benchmark vs Peers ───────────────────────────────────────────────────
    st.markdown("---")
    section("Benchmark vs Global & Regional Average")

    bench_domains = []
    for dom in domains_list:
        c_val = float(c_a7[dom].values[0]) if (not c_a7.empty and dom in c_a7.columns
                                                and not pd.isna(c_a7[dom].values[0])) else None
        g_val = float(A3[A3['Domain'] == dom]['Global Domain Average'].values[0]) \
                if len(A3[A3['Domain'] == dom]) > 0 else None
        r_val_s = fct[(fct['Region'] == c_region) & (fct['Domain'] == dom)]['Normalized Value'].mean()
        r_val = round(float(r_val_s), 4) if not pd.isna(r_val_s) else None
        bench_domains.append({
            'Domain': dom,
            sel_country: c_val,
            'Global Avg': g_val,
            f'{c_region} Avg': r_val,
        })
    bench_df = pd.DataFrame(bench_domains)

    fig_bench = go.Figure()
    for col, clr in [(sel_country, C["blue"]), ('Global Avg', C["grey"]), (f'{c_region} Avg', C["gold"])]:
        fig_bench.add_trace(go.Bar(
            name=col, x=bench_df['Domain'], y=bench_df[col],
            marker_color=clr, opacity=0.85,
        ))
    fig_bench.update_layout(barmode='group', xaxis_title='Domain',
                            yaxis_title='Avg Normalized Score',
                            yaxis_range=[0, 1.05])
    theme(fig_bench, height=320)
    st.plotly_chart(fig_bench, use_container_width=True)

    # ── Filtered Ranking ─────────────────────────────────────────────────────
    st.markdown("---")
    section("Country Ranking Table", f"{len(filtered)} countries match the current filters.")

    top_n  = (filtered.sort_values('Composite Resilience Score', ascending=False)
              .head(15).sort_values('Composite Resilience Score'))
    bot_n  = (filtered.sort_values('Composite Resilience Score').head(15))

    fc1, fc2 = st.columns(2)
    with fc1:
        st.caption("🏆 Top 15 (filtered)")
        fig_top = go.Figure(go.Bar(
            x=top_n['Composite Resilience Score'], y=top_n['Country Name'],
            orientation='h',
            marker_color=[REGION_COLORS.get(r, C["blue"]) for r in top_n['Region']],
            text=top_n['Composite Resilience Score'].map('{:.3f}'.format),
            textposition='outside',
        ))
        fig_top.add_vline(x=0.5, line_dash="dash", line_color=C["red"])
        fig_top.update_layout(xaxis_range=[0, 1.0], xaxis_title="Score", yaxis_title="")
        theme(fig_top, height=420)
        st.plotly_chart(fig_top, use_container_width=True)

    with fc2:
        st.caption("⚠️ Bottom 15 (filtered)")
        fig_bot = go.Figure(go.Bar(
            x=bot_n['Composite Resilience Score'], y=bot_n['Country Name'],
            orientation='h',
            marker_color=[REGION_COLORS.get(r, C["red"]) for r in bot_n['Region']],
            text=bot_n['Composite Resilience Score'].map('{:.3f}'.format),
            textposition='outside',
        ))
        fig_bot.add_vline(x=0.5, line_dash="dash", line_color=C["red"])
        fig_bot.update_layout(xaxis_range=[0, 1.0], xaxis_title="Score", yaxis_title="")
        theme(fig_bot, height=420)
        st.plotly_chart(fig_bot, use_container_width=True)

    # ── Decade Improvement ───────────────────────────────────────────────────
    st.markdown("---")
    section("Top 20 Most Improved Countries (2000s → 2020s)")
    if 'Decade_Improvement' in A13.columns:
        top_imp = A13.dropna(subset=['Decade_Improvement']).head(20).copy()
        top_imp = top_imp.sort_values('Decade_Improvement', ascending=True)
        fig_imp = go.Figure(go.Bar(
            x=top_imp['Decade_Improvement'], y=top_imp['Country Name'],
            orientation='h',
            marker_color=[C["green"] if v >= 0 else C["red"]
                          for v in top_imp['Decade_Improvement']],
            text=top_imp['Decade_Improvement'].map('{:+.4f}'.format),
            textposition='outside',
        ))
        fig_imp.update_layout(xaxis_title="Score Improvement (2020s − 2000s)", yaxis_title="")
        theme(fig_imp, height=480)
        st.plotly_chart(fig_imp, use_container_width=True)

    st.markdown("---")
    st.dataframe(
        filtered[['Rank', 'Country Name', 'Region',
                  'Composite Resilience Score', 'Resilience Tier']],
        use_container_width=True, hide_index=True,
    )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 3 — REGIONAL ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ Regional Analysis":
    st.title("🗺️ Regional Analysis")
    st.caption("Compare resilience performance across 9 world regions.")

    # ── Region KPIs ──────────────────────────────────────────────────────────
    rk1, rk2, rk3 = st.columns(3)
    kpi_card(rk1, "Best Region",             kpis['top_region'])
    kpi_card(rk2, "Weakest Region",           kpis['lowest_region'])
    kpi_card(rk3, "Fastest Improving Region", kpis['fastest_improving_region'])

    # Fastest improving region insight
    reg_decade = (fct.groupby(['Region', 'Decade'])['Normalized Value']
                  .mean().unstack('Decade').round(4))
    reg_decade.columns.name = None
    if '2000s' in reg_decade.columns and '2020s' in reg_decade.columns:
        reg_decade['Improvement'] = (reg_decade['2020s'] - reg_decade['2000s']).round(4)
        best_reg_imp = reg_decade['Improvement'].max()
        insight_box(
            f"<b>{kpis['fastest_improving_region']}</b> improved its average resilience score by "
            f"<b>+{best_reg_imp:.3f}</b> between the 2000s and the 2020s — the fastest trajectory of any region.",
            "📈"
        )

    st.markdown("---")

    # ── Region Ranking Bar ────────────────────────────────────────────────────
    section("Region Composite Resilience Score")
    a18s = A18.sort_values('Region_Resilience_Score', ascending=True)
    fig_reg = go.Figure(go.Bar(
        x=a18s['Region_Resilience_Score'], y=a18s['Region'],
        orientation='h',
        marker_color=[REGION_COLORS.get(r, C["blue"]) for r in a18s['Region']],
        text=a18s['Region_Resilience_Score'].map('{:.4f}'.format),
        textposition='outside',
        customdata=a18s['Country_Count'],
        hovertemplate='%{y}<br>Score: %{x:.4f}<br>Countries: %{customdata}<extra></extra>',
    ))
    fig_reg.add_vline(x=0.5, line_dash="dash", line_color=C["red"],
                      annotation_text="Risk threshold 0.50")
    fig_reg.update_layout(xaxis_range=[0, 0.95], xaxis_title="Avg Normalized Score", yaxis_title="")
    theme(fig_reg, height=340)
    st.plotly_chart(fig_reg, use_container_width=True)

    # ── Region × Domain Heatmap ───────────────────────────────────────────────
    section("Region × Domain Heatmap",
            "Which domains are each region's strength or weakness?")
    pivot_heat = A4.pivot(index='Region', columns='Domain', values='Avg Resilience Score')
    fig_heat = px.imshow(
        pivot_heat,
        color_continuous_scale='RdYlGn',
        zmin=0, zmax=1,
        text_auto='.3f',
        aspect='auto',
    )
    fig_heat.update_coloraxes(colorbar_title="Score")
    fig_heat.update_layout(xaxis_title="", yaxis_title="",
                           xaxis_tickangle=-30)
    theme(fig_heat, height=360)
    st.plotly_chart(fig_heat, use_container_width=True)

    # ── Region × Year Trend ───────────────────────────────────────────────────
    st.markdown("---")
    section("Resilience Trend by Region (2000–2023)")
    region_year = (fct.groupby(['Region', 'Year'])['Normalized Value']
                   .mean().round(4).reset_index()
                   .rename(columns={'Normalized Value': 'Avg Resilience'}))
    region_filter = st.multiselect(
        "Select regions to display",
        options=sorted(region_year['Region'].unique().tolist()),
        default=sorted(region_year['Region'].unique().tolist()),
    )
    ry_filtered = region_year[region_year['Region'].isin(region_filter)]
    fig_ryt = go.Figure()
    for reg in region_filter:
        rdf = ry_filtered[ry_filtered['Region'] == reg]
        fig_ryt.add_scatter(x=rdf['Year'], y=rdf['Avg Resilience'],
                            mode='lines', name=reg,
                            line=dict(color=REGION_COLORS.get(reg, C["blue"]), width=2))
    fig_ryt.add_hline(y=0.5, line_dash="dash", line_color=C["red"])
    fig_ryt.update_layout(xaxis_title="Year", yaxis_title="Avg Resilience",
                          yaxis_range=[0.2, 0.85])
    theme(fig_ryt, height=380)
    st.plotly_chart(fig_ryt, use_container_width=True)

    # ── Region Drill-Down ─────────────────────────────────────────────────────
    st.markdown("---")
    sel_reg2 = st.selectbox("Drill into Region", sorted(A1['Region'].unique().tolist()))
    reg_countries = A1[A1['Region'] == sel_reg2].copy()

    insight_box(
        f"<b>{sel_reg2}</b> contains <b>{len(reg_countries)}</b> countries in this study. "
        f"Average score: <b>{reg_countries['Composite Resilience Score'].mean():.4f}</b>. "
        f"Leader: <b>{reg_countries.iloc[0]['Country Name']} ({reg_countries.iloc[0]['Composite Resilience Score']:.3f})</b>."
    )

    rc_sorted = reg_countries.sort_values('Composite Resilience Score', ascending=True)
    tier_c = [TIER_COLORS.get(
        str(A20[A20['Country Name'] == cn]['Resilience Tier'].values[0]), C["blue"])
              for cn in rc_sorted['Country Name']]
    fig_drill = go.Figure(go.Bar(
        x=rc_sorted['Composite Resilience Score'], y=rc_sorted['Country Name'],
        orientation='h', marker_color=tier_c,
        text=rc_sorted['Composite Resilience Score'].map('{:.3f}'.format),
        textposition='outside',
    ))
    fig_drill.add_vline(x=0.5, line_dash="dash", line_color=C["red"])
    fig_drill.update_layout(xaxis_range=[0, 1.0], xaxis_title="Composite Score", yaxis_title="")
    theme(fig_drill, height=max(300, len(reg_countries) * 28))
    st.plotly_chart(fig_drill, use_container_width=True)

    # ── Decade improvement by region ─────────────────────────────────────────
    if 'Improvement' in reg_decade.columns:
        st.markdown("---")
        section("Region Improvement: 2000s → 2020s")
        rd = reg_decade[['2000s', '2020s', 'Improvement']].dropna().reset_index()
        rd = rd.sort_values('Improvement', ascending=True)
        fig_rimp = go.Figure(go.Bar(
            x=rd['Improvement'], y=rd['Region'],
            orientation='h',
            marker_color=[C["green"] if v >= 0 else C["red"] for v in rd['Improvement']],
            text=rd['Improvement'].map('{:+.4f}'.format),
            textposition='outside',
        ))
        fig_rimp.update_layout(xaxis_title="Score Change (2020s − 2000s)", yaxis_title="")
        theme(fig_rimp, height=300)
        st.plotly_chart(fig_rimp, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 4 — RISK & STABILITY
# ═════════════════════════════════════════════════════════════════════════════
elif page == "⚠️ Risk & Stability":
    st.title("⚠️ Risk & Stability")
    st.caption("Identify fragile states, political instability, economic shocks, and double-exposure countries.")

    # ── KPIs ─────────────────────────────────────────────────────────────────
    rs1, rs2, rs3, rs4 = st.columns(4)
    kpi_card(rs1, "High-Risk Countries",  str(kpis['high_risk_count']),
             delta="score < 0.5", delta_color="inverse")
    kpi_card(rs2, "Stable Countries",      str(kpis['stable_count']))
    kpi_card(rs3, "Weakest Domain",        kpis['weakest_domain'])
    kpi_card(rs4, "Avg Risk Score",        f"{kpis['avg_risk']:.4f}")

    insight_box(
        f"<b>{kpis['high_risk_count']}</b> of {kpis['total_countries']} countries score below the 0.50 risk threshold. "
        f"The weakest global domain — <b>{kpis['weakest_domain']}</b> — is the primary systemic driver of fragility.",
        "🔴"
    )

    # ── Risk Drivers ─────────────────────────────────────────────────────────
    st.markdown("---")
    section("Risk Drivers by Domain",
            "What makes high-risk countries fragile? Domain breakdown for high-risk vs stable countries.")

    # Average domain scores for high-risk vs stable groups
    hr_countries  = A8['Country Name'].tolist()
    stb_countries = A9['Country Name'].tolist()
    hr_dom  = (fct[fct['Country Name'].isin(hr_countries)]
               .groupby('Domain')['Normalized Value'].mean().round(4))
    stb_dom = (fct[fct['Country Name'].isin(stb_countries)]
               .groupby('Domain')['Normalized Value'].mean().round(4))
    driver_df = pd.DataFrame({
        'Domain': hr_dom.index,
        'High-Risk Avg': hr_dom.values,
        'Stable Avg': stb_dom.reindex(hr_dom.index).values,
    })

    fig_drivers = go.Figure()
    fig_drivers.add_trace(go.Bar(
        name='High-Risk Countries', x=driver_df['Domain'], y=driver_df['High-Risk Avg'],
        marker_color=C["red"], opacity=0.85,
    ))
    fig_drivers.add_trace(go.Bar(
        name='Stable Countries', x=driver_df['Domain'], y=driver_df['Stable Avg'],
        marker_color=C["green"], opacity=0.85,
    ))
    fig_drivers.update_layout(barmode='group', xaxis_title='Domain',
                              yaxis_title='Avg Normalized Score', yaxis_range=[0, 1.0])
    theme(fig_drivers, height=320)
    st.plotly_chart(fig_drivers, use_container_width=True)

    # Insight on the biggest gap
    if not driver_df.empty:
        driver_df['Gap'] = driver_df['Stable Avg'] - driver_df['High-Risk Avg']
        worst_gap_domain = driver_df.loc[driver_df['Gap'].idxmax(), 'Domain']
        worst_gap_val    = driver_df['Gap'].max()
        insight_box(
            f"The largest gap between stable and high-risk countries is in "
            f"<b>{worst_gap_domain}</b> — stable countries score <b>{worst_gap_val:.3f}</b> higher. "
            f"This is the most discriminating domain for resilience.",
            "🔍"
        )

    st.markdown("---")

    # ── Political Stability Trend ────────────────────────────────────────────
    section("Political Stability — Global Trend (2000–2023)",
            "World Bank PV.EST indicator. Negative = instability. Zero = neutral.")
    fig_pol = go.Figure()
    fig_pol.add_scatter(x=A15['Year'], y=A15['Avg Political Stability Index'],
                        mode='lines+markers', name='Pol. Stability',
                        line=dict(color=C["gold"], width=2),
                        marker=dict(size=5),
                        fill='tozeroy',
                        fillcolor='rgba(243,156,18,0.08)')
    fig_pol.add_hline(y=0, line_dash="dash", line_color=C["red"],
                      annotation_text="Neutral 0", annotation_font_color=C["red"])
    fig_pol.update_layout(xaxis_title="Year", yaxis_title="Avg WB Political Stability Score")
    theme(fig_pol, height=300)
    st.plotly_chart(fig_pol, use_container_width=True)

    # ── High Risk + Unstable columns ─────────────────────────────────────────
    rc1, rc2 = st.columns(2)

    with rc1:
        section("High-Risk Countries (Score < 0.50)")
        show_hr = A8.sort_values('Composite Score').copy()
        fig_hr = go.Figure(go.Bar(
            x=show_hr['Composite Score'], y=show_hr['Country Name'],
            orientation='h',
            marker_color=[REGION_COLORS.get(r, C["red"]) for r in show_hr['Region']],
            text=show_hr['Composite Score'].map('{:.3f}'.format),
            textposition='outside',
        ))
        fig_hr.add_vline(x=0.5, line_dash="dash", line_color=C["grey"])
        fig_hr.update_layout(xaxis_range=[0, 0.65], xaxis_title="Composite Score", yaxis_title="")
        theme(fig_hr, height=max(300, len(show_hr) * 20))
        st.plotly_chart(fig_hr, use_container_width=True)

    with rc2:
        if not A33.empty:
            section("Most Politically Unstable Countries",
                    "Avg WB Political Stability Index below −0.5")
            show_a33 = A33.head(20).sort_values('Avg_Pol_Stability')
            fig_pol2 = go.Figure(go.Bar(
                x=show_a33['Avg_Pol_Stability'], y=show_a33['Country Name'],
                orientation='h',
                marker_color=[REGION_COLORS.get(r, C["red"]) for r in show_a33['Region']],
                text=show_a33['Avg_Pol_Stability'].map('{:.3f}'.format),
                textposition='outside',
            ))
            fig_pol2.add_vline(x=0, line_dash="dash", line_color=C["grey"])
            fig_pol2.update_layout(xaxis_title="Avg WB Pol. Stability Score", yaxis_title="")
            theme(fig_pol2, height=max(300, len(show_a33) * 20))
            st.plotly_chart(fig_pol2, use_container_width=True)

    # ── GDP Shock Detection ───────────────────────────────────────────────────
    st.markdown("---")
    section("GDP Growth — Global Average & Shock Detection",
            "Negative years = economic contraction. 2020 COVID shock clearly visible.")
    fig_gdp = go.Figure()
    fig_gdp.add_bar(
        x=A24['Year'], y=A24['Avg'],
        marker_color=[C["red"] if v < 0 else C["green"] for v in A24['Avg']],
        name='Avg GDP Growth %',
        hovertemplate='Year: %{x}<br>Avg: %{y:.2f}%<extra></extra>',
    )
    fig_gdp.add_scatter(x=A24['Year'], y=A24['Avg'], mode='lines',
                        line=dict(color=C["blue"], width=1.5), name='Trend')
    fig_gdp.add_vline(x=2020, line_dash="dash", line_color=C["red"],
                      annotation_text="COVID-19 (2020)", annotation_font_color=C["red"])
    fig_gdp.update_layout(xaxis_title="Year", yaxis_title="Avg GDP Growth %")
    theme(fig_gdp, height=300)
    st.plotly_chart(fig_gdp, use_container_width=True)

    # ── Double Exposure Scatter ───────────────────────────────────────────────
    st.markdown("---")
    section("Double Exposure — Healthcare vs Undernourishment",
            "Top-left quadrant: high healthcare score but high undernourishment. "
            "Bottom-left: DOUBLE RISK — weak healthcare AND high undernourishment.")
    double_count = int((A22['Exposure Type'] == 'Double Risk').sum())
    insight_box(
        f"<b>{double_count} countries</b> face double exposure: both below-average healthcare "
        f"(score < 0.4) AND high undernourishment (> 10%). These countries face compound humanitarian risk.",
        "⚠️"
    )
    fig_exp = px.scatter(
        A22, x='Healthcare Score', y='Avg Undernourishment %',
        color='Exposure Type', hover_name='Country Name',
        hover_data=['Region'],
        color_discrete_map={'Double Risk': C["red"], 'Single / No Risk': C["blue"]},
        opacity=0.85, size_max=12,
    )
    fig_exp.add_vline(x=0.4, line_dash="dot", line_color=C["grey"],
                      annotation_text="Healthcare 0.4")
    fig_exp.add_hline(y=10, line_dash="dot", line_color=C["grey"],
                      annotation_text="Undernourishment 10%")
    fig_exp.update_layout(xaxis_title="Healthcare Score (normalized)",
                          yaxis_title="Avg Undernourishment %")
    theme(fig_exp, height=380)
    st.plotly_chart(fig_exp, use_container_width=True)

    # ── Full Risk Sheet ───────────────────────────────────────────────────────
    st.markdown("---")
    section("Full Risk Score Sheet", "A36 — all 100 countries with domain-level scores.")
    st.dataframe(A36, use_container_width=True, hide_index=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 5 — FOOD SECURITY
# ═════════════════════════════════════════════════════════════════════════════
elif page == "🌾 Food Security":
    st.title("🌾 Food Security")
    st.caption("Food price shocks, country vulnerability, commodity trends, and undernourishment risk.")

    # ── KPIs ─────────────────────────────────────────────────────────────────
    fs1, fs2, fs3, fs4 = st.columns(4)
    kpi_card(fs1, "Food Dependency Rate",     f"{kpis['food_dependency']:.2f}%",
             help_text="Avg food imports as % of merchandise imports")
    kpi_card(fs2, "Food Vulnerability Score", f"{kpis['food_vulnerability']:.4f}",
             help_text="Avg normalized food security score (lower = more vulnerable)")
    kpi_card(fs3, "Avg Undernourishment",     f"{kpis['undernourishment']:.2f}%")
    double_count = int((A22['Exposure Type'] == 'Double Risk').sum())
    kpi_card(fs4, "Double-Risk Countries",    str(double_count),
             delta="health + food", delta_color="inverse")

    # ── Food Security country rankings ────────────────────────────────────────
    st.markdown("---")
    food_country = (fct[fct['Domain'] == 'Food Security']
                    .groupby(['Country Name', 'Region'])['Normalized Value']
                    .mean().round(4).reset_index()
                    .rename(columns={'Normalized Value': 'Food Security Score'}))
    food_top = food_country.sort_values('Food Security Score', ascending=False).head(15)
    food_bot = food_country.sort_values('Food Security Score').head(15)

    ft1, ft2 = st.columns(2)
    with ft1:
        section("🏆 Most Food-Secure Countries")
        fig_ft = go.Figure(go.Bar(
            x=food_top.sort_values('Food Security Score')['Food Security Score'],
            y=food_top.sort_values('Food Security Score')['Country Name'],
            orientation='h',
            marker_color=[REGION_COLORS.get(r, C["green"]) for r in
                          food_top.sort_values('Food Security Score')['Region']],
            text=food_top.sort_values('Food Security Score')['Food Security Score'].map('{:.3f}'.format),
            textposition='outside',
        ))
        fig_ft.update_layout(xaxis_range=[0, 1.05], xaxis_title="Food Security Score", yaxis_title="")
        theme(fig_ft, height=400)
        st.plotly_chart(fig_ft, use_container_width=True)

    with ft2:
        section("⚠️ Most Food-Vulnerable Countries")
        fig_fb = go.Figure(go.Bar(
            x=food_bot['Food Security Score'], y=food_bot['Country Name'],
            orientation='h',
            marker_color=[REGION_COLORS.get(r, C["red"]) for r in food_bot['Region']],
            text=food_bot['Food Security Score'].map('{:.3f}'.format),
            textposition='outside',
        ))
        fig_fb.update_layout(xaxis_range=[0, 1.05], xaxis_title="Food Security Score", yaxis_title="")
        theme(fig_fb, height=400)
        st.plotly_chart(fig_fb, use_container_width=True)

    if not fi.empty:
        # ── FAO Commodity Trend ────────────────────────────────────────────────
        st.markdown("---")
        section("FAO Food Price Index — All Commodities (2000–2023)",
                "Annual average. 100 = reference baseline. Spike in 2022 driven by Russia-Ukraine war.")

        annual_fao = fi.groupby(['Year', 'Type'])['Price Index'].mean().reset_index()
        comm_colors = {
            'Food': C["gold"], 'Meat': C["red"], 'Dairy': C["blue"],
            'Cereals': C["green"], 'Oils': C["purple"], 'Sugar': C["teal"],
        }
        fig_fao = go.Figure()
        for t in annual_fao['Type'].unique():
            td = annual_fao[annual_fao['Type'] == t]
            fig_fao.add_scatter(x=td['Year'], y=td['Price Index'],
                                mode='lines', name=t,
                                line=dict(color=comm_colors.get(t, C["grey"]), width=2))
        fig_fao.add_vline(x=2022, line_dash="dash", line_color=C["red"],
                          annotation_text="2022 Shock", annotation_font_color=C["red"])
        fig_fao.add_vline(x=2020, line_dash="dot",  line_color=C["gold"],
                          annotation_text="COVID-19", annotation_font_color=C["gold"])
        fig_fao.update_layout(xaxis_title="Year", yaxis_title="Price Index (avg monthly)",
                              legend=dict(orientation='h', y=-0.15))
        theme(fig_fao, height=340)
        st.plotly_chart(fig_fao, use_container_width=True)

        # ── 2022 Shock + Commodity Spotlight ──────────────────────────────────
        sc1, sc2 = st.columns(2)

        with sc1:
            section("2022 Food Price Shock — % Change vs 2020",
                    "Russia-Ukraine war drove historically high price spikes across all commodities.")
            if not A25.empty:
                a25s = A25.sort_values('Pct_Change_vs_2020', ascending=True)
                fig_shock = go.Figure(go.Bar(
                    x=a25s['Pct_Change_vs_2020'], y=a25s['Type'],
                    orientation='h',
                    marker_color=[C["red"] if v > 0 else C["green"]
                                  for v in a25s['Pct_Change_vs_2020']],
                    text=a25s['Pct_Change_vs_2020'].map('{:+.1f}%'.format),
                    textposition='outside',
                ))
                fig_shock.add_vline(x=0, line_dash="solid", line_color=C["grey"])
                fig_shock.update_layout(xaxis_title="% Change vs 2020", yaxis_title="")
                theme(fig_shock, height=320)
                st.plotly_chart(fig_shock, use_container_width=True)

        with sc2:
            section("Commodity Spotlight")
            commodity_list = sorted(fi['Type'].unique().tolist())
            sel_commodity = st.selectbox("Select Commodity", commodity_list)
            comm_data = (fi[fi['Type'] == sel_commodity]
                         .groupby('Year')['Price Index'].mean().reset_index())
            peak_year  = int(comm_data.loc[comm_data['Price Index'].idxmax(), 'Year'])
            peak_val   = comm_data['Price Index'].max()
            fig_comm = go.Figure()
            fig_comm.add_scatter(x=comm_data['Year'], y=comm_data['Price Index'],
                                 mode='lines+markers', name=sel_commodity,
                                 line=dict(color=comm_colors.get(sel_commodity, C["gold"]), width=2.5),
                                 fill='tozeroy',
                                 fillcolor=f'rgba(243,156,18,0.08)')
            fig_comm.add_vline(x=peak_year, line_dash="dash", line_color=C["red"],
                               annotation_text=f"Peak {peak_year}: {peak_val:.0f}")
            fig_comm.update_layout(xaxis_title="Year", yaxis_title="Avg Price Index")
            theme(fig_comm, height=320)
            st.plotly_chart(fig_comm, use_container_width=True)

        # ── Price Category Distribution ────────────────────────────────────────
        st.markdown("---")
        section("Price Category Distribution by Commodity",
                "How many months each commodity spent in each price bracket.")
        cat_order = [
            'Extremely Cheap','Very Cheap','Cheap','Slightly Cheap','Below Normal',
            'Near Normal','Slightly Expensive','Moderately Expensive','Expensive','Very Expensive',
        ]
        cat_colors = ['#1a7f4b','#2da65f','#48C98E','#8fd4b0','#c4e0d3',
                      '#e8e8e8','#f4c56e','#f4a261','#e05c5c','#9b2226']
        cat_color_map = dict(zip(cat_order, cat_colors))
        cat_dist = fi.groupby(['Type', 'Price Category']).size().reset_index(name='Count')
        fig_cat = px.bar(
            cat_dist, x='Type', y='Count', color='Price Category',
            color_discrete_map=cat_color_map,
            category_orders={'Price Category': cat_order},
        )
        fig_cat.update_layout(xaxis_title="Commodity", yaxis_title="Number of Months",
                              legend_title="Price Category",
                              legend=dict(orientation='h', y=-0.25))
        theme(fig_cat, height=380)
        st.plotly_chart(fig_cat, use_container_width=True)

    # ── Double Exposure ────────────────────────────────────────────────────────
    st.markdown("---")
    section("Double-Risk Countries — Healthcare + Undernourishment",
            "Countries flagged with simultaneous healthcare vulnerability AND high undernourishment.")
    double_risk = A22[A22['Exposure Type'] == 'Double Risk'].copy()
    if double_risk.empty:
        st.info("No countries meet the double-risk threshold in this dataset.")
    else:
        st.dataframe(
            double_risk[['Country Name', 'Region', 'Healthcare Score',
                         'Avg Undernourishment %', 'Exposure Type']],
            use_container_width=True, hide_index=True,
        )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 6 — FUTURE SHOCK INDEX
# ═════════════════════════════════════════════════════════════════════════════
elif page == "⚡ Future Shock Index":
    st.title("⚡ Future Shock Index")
    st.caption(
        "Which countries are most exposed to future global shocks? "
        "Built from existing domain scores — no new calculations."
    )

    insight_box(
        "The Future Shock Index scores each country's exposure to four shock vectors: "
        "food vulnerability, political instability, economic fragility, and climate pressure. "
        "All scores are derived directly from the existing normalized domain data.",
        "⚡"
    )

    # ── Build Future Shock Score ──────────────────────────────────────────────
    # Uses A7 domain pivot + A33 (political) — no new calculations, just recombination
    fsi_base = A7[['Country Name', 'Region', 'Composite Score']].copy()

    domains_in_a7 = ['Food Security', 'Political Stability', 'Economic Fragility', 'Climate & Energy']
    for dom in domains_in_a7:
        if dom in A7.columns:
            fsi_base[dom] = A7[dom].values

    # Shock exposure = 1 - domain score (higher = more exposed / more vulnerable)
    fsi = fsi_base.copy()
    shock_cols = []
    for dom in domains_in_a7:
        if dom in fsi.columns:
            col = f'{dom} Exposure'
            fsi[col] = (1 - fsi[dom]).round(4)
            shock_cols.append(col)

    if shock_cols:
        fsi['Future Shock Score'] = fsi[shock_cols].mean(axis=1).round(4)
        fsi = fsi.sort_values('Future Shock Score', ascending=False).reset_index(drop=True)
        fsi.insert(0, 'Shock Rank', range(1, len(fsi) + 1))
    else:
        fsi['Future Shock Score'] = np.nan
        fsi['Shock Rank'] = np.nan

    # Segment: very high / high / moderate / low
    fsi['Shock Level'] = pd.cut(
        fsi['Future Shock Score'],
        bins=[-np.inf, 0.30, 0.45, 0.60, np.inf],
        labels=['Low Exposure', 'Moderate', 'High Exposure', 'Very High Exposure'],
    )

    # ── KPIs ─────────────────────────────────────────────────────────────────
    fsi_valid = fsi.dropna(subset=['Future Shock Score'])
    most_exposed    = fsi_valid.iloc[0]['Country Name']  if len(fsi_valid) > 0 else 'N/A'
    least_exposed   = fsi_valid.iloc[-1]['Country Name'] if len(fsi_valid) > 0 else 'N/A'
    very_high_count = int((fsi_valid['Shock Level'].astype(str) == 'Very High Exposure').sum())
    low_count       = int((fsi_valid['Shock Level'].astype(str) == 'Low Exposure').sum())

    fk1, fk2, fk3, fk4 = st.columns(4)
    kpi_card(fk1, "Most Exposed Country",   most_exposed)
    kpi_card(fk2, "Least Exposed Country",  least_exposed)
    kpi_card(fk3, "Very High Exposure",      str(very_high_count),
             delta="countries", delta_color="inverse")
    kpi_card(fk4, "Low Exposure",            str(low_count), delta="countries")

    st.markdown("---")

    # ── Top 20 Most Vulnerable ────────────────────────────────────────────────
    section("Top 25 Most Shock-Exposed Countries",
            "Ranked by composite Future Shock Score (avg of food, political, economic, climate exposure).")

    top_fsi = fsi_valid.head(25).sort_values('Future Shock Score', ascending=True)
    fig_fsi = go.Figure(go.Bar(
        x=top_fsi['Future Shock Score'], y=top_fsi['Country Name'],
        orientation='h',
        marker_color=[REGION_COLORS.get(r, C["red"]) for r in top_fsi['Region']],
        text=top_fsi['Future Shock Score'].map('{:.3f}'.format),
        textposition='outside',
    ))
    fig_fsi.update_layout(xaxis_range=[0, 0.85], xaxis_title="Future Shock Score (higher = more exposed)",
                          yaxis_title="")
    theme(fig_fsi, height=580)
    st.plotly_chart(fig_fsi, use_container_width=True)

    # ── Least Vulnerable 15 ───────────────────────────────────────────────────
    st.markdown("---")
    section("15 Least Shock-Exposed Countries", "Countries with the strongest all-round buffers.")
    low_fsi = fsi_valid.tail(15).sort_values('Future Shock Score', ascending=False)
    fig_low = go.Figure(go.Bar(
        x=low_fsi['Future Shock Score'], y=low_fsi['Country Name'],
        orientation='h',
        marker_color=[REGION_COLORS.get(r, C["green"]) for r in low_fsi['Region']],
        text=low_fsi['Future Shock Score'].map('{:.3f}'.format),
        textposition='outside',
    ))
    fig_low.update_layout(xaxis_range=[0, 0.55], xaxis_title="Future Shock Score",
                          yaxis_title="")
    theme(fig_low, height=380)
    st.plotly_chart(fig_low, use_container_width=True)

    # ── Shock Level Donut ────────────────────────────────────────────────────
    c1, c2 = st.columns(2)

    with c1:
        section("Countries by Shock Exposure Level")
        sl_order  = ['Very High Exposure', 'High Exposure', 'Moderate', 'Low Exposure']
        sl_colors = [C["red"], C["gold"], C["blue"], C["green"]]
        sl_counts = (fsi_valid['Shock Level'].astype(str)
                     .value_counts().reindex(sl_order, fill_value=0)
                     .reset_index())
        sl_counts.columns = ['Level', 'Count']
        fig_sl = go.Figure(go.Pie(
            labels=sl_counts['Level'], values=sl_counts['Count'],
            hole=0.55,
            marker_colors=sl_colors,
            sort=False,
            textinfo='label+value',
        ))
        fig_sl.update_layout(showlegend=False)
        theme(fig_sl, height=300)
        st.plotly_chart(fig_sl, use_container_width=True)

    with c2:
        section("Shock Exposure by Region")
        reg_fsi = (fsi_valid.groupby('Region')['Future Shock Score']
                   .mean().round(4).sort_values(ascending=True).reset_index())
        fig_rfsi = go.Figure(go.Bar(
            x=reg_fsi['Future Shock Score'], y=reg_fsi['Region'],
            orientation='h',
            marker_color=[REGION_COLORS.get(r, C["red"]) for r in reg_fsi['Region']],
            text=reg_fsi['Future Shock Score'].map('{:.3f}'.format),
            textposition='outside',
        ))
        fig_rfsi.update_layout(xaxis_range=[0, 0.75],
                               xaxis_title="Avg Future Shock Score", yaxis_title="")
        theme(fig_rfsi, height=300)
        st.plotly_chart(fig_rfsi, use_container_width=True)

    # ── Shock Component Breakdown ──────────────────────────────────────────────
    st.markdown("---")
    section("Shock Exposure Component Breakdown — Top 20",
            "Which shock vector is the biggest threat for each high-exposure country?")
    top20_fsi = fsi_valid.head(20).copy()
    comp_cols = [c for c in shock_cols if c in top20_fsi.columns]
    if comp_cols:
        fig_comp = go.Figure()
        comp_display = {
            'Food Security Exposure':       C["gold"],
            'Political Stability Exposure': C["purple"],
            'Economic Fragility Exposure':  C["red"],
            'Climate & Energy Exposure':    C["teal"],
        }
        for col, clr in comp_display.items():
            if col in top20_fsi.columns:
                fig_comp.add_trace(go.Bar(
                    name=col.replace(' Exposure', ''),
                    x=top20_fsi['Country Name'],
                    y=top20_fsi[col],
                    marker_color=clr,
                    opacity=0.85,
                ))
        fig_comp.update_layout(barmode='stack', xaxis_title="Country",
                               yaxis_title="Exposure Score",
                               xaxis_tickangle=-35,
                               legend=dict(orientation='h', y=-0.25))
        theme(fig_comp, height=400)
        st.plotly_chart(fig_comp, use_container_width=True)

    # ── Full table ────────────────────────────────────────────────────────────
    st.markdown("---")
    section("Full Future Shock Index Table")
    display_cols = ['Shock Rank', 'Country Name', 'Region', 'Future Shock Score', 'Shock Level'] + \
                   [c for c in shock_cols if c in fsi.columns]
    st.dataframe(fsi[display_cols], use_container_width=True, hide_index=True)
