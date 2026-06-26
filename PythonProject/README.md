# 🌍 Global Resilience Index

> Measuring how countries withstand economic, social, environmental, and political shocks through a comprehensive data-driven resilience framework.

---

## 📖 Project Overview

The **Global Resilience Index** is an end-to-end data analytics project designed to evaluate and compare the resilience of 100 countries across six critical domains.

Using World Bank and FAO datasets, the project transforms raw socio-economic, environmental, and political indicators into a unified resilience framework that highlights how countries respond to economic, food, healthcare, climate, and governance challenges.

The dashboard provides a comprehensive view of global resilience trends, regional performance, country rankings, risk exposure, and future vulnerability assessment from 2000 to 2023.

Beyond simple ranking, the project uncovers **hidden patterns of resilience**, showing how countries with similar economic levels can perform very differently depending on governance quality, infrastructure readiness, and social stability.

---

## 🎯 Project Objectives

* Build a comprehensive Global Resilience Framework.
* Measure resilience across multiple dimensions.
* Compare countries and regions using a unified scoring methodology.
* Identify high-risk and vulnerable countries.
* Analyze long-term resilience trends.
* Evaluate preparedness for future global shocks.
* Transform complex datasets into actionable insights.
* Reveal structural weaknesses that may not be visible through traditional economic indicators alone.

---

## 🏗️ Resilience Framework

The index is built around six major domains:

| Domain                    | Description                                       |
| ------------------------- | ------------------------------------------------- |
| 💻 Digital Infrastructure | Internet users and broadband accessibility        |
| 📉 Economic Fragility     | GDP growth and inflation indicators               |
| 🌾 Food Security          | Food imports and undernourishment metrics         |
| 🏥 Healthcare             | Healthcare expenditure, hospitals, and physicians |
| 🏛️ Political Stability   | Governance and political stability indicators     |
| ⚡ Climate & Energy        | Energy access, renewable energy, and emissions    |

Each domain captures a **critical pillar of resilience**, and together they provide a holistic view of how countries absorb shocks, adapt to disruptions, and recover over time.

---

## 📊 Dashboard Pages

### 🌐 Overview


images/overview.png

Provides executive-level insights including:

* Global resilience trends
* Key performance indicators
* Domain performance comparison
* Resilience tiers
* Decade analysis

**Insights Added:**

* Identifies global shifts in resilience before and after major crises (e.g., financial crises, pandemics).
* Highlights widening or narrowing gaps between high-performing and low-performing countries.
* Shows which domains are driving global improvement or decline.

---

### 🔍 Country Explorer


images/country_explorer.png

Allows users to:

* Explore individual countries
* View resilience scorecards
* Compare against regional and global averages
* Analyze country trends over time
* Benchmark domain performance

**Insights Added:**

* Detects whether a country’s resilience is balanced or dependent on a single strong domain.
* Reveals hidden vulnerabilities even in high-ranking countries.
* Tracks recovery speed after economic or political shocks.

---

### 🗺️ Regional Analysis


images/regional_analysis.png

Focuses on:

* Regional rankings
* Region vs domain performance
* Heatmaps
* Regional resilience trends
* Improvement analysis

**Insights Added:**

* Identifies leading and lagging regions in specific domains.
* Highlights regional disparities and structural inequalities.
* Shows which regions are improving fastest and which are stagnating.

---

### ⚠️ Risk & Stability


images/risk_stability.png

Highlights:

* High-risk countries
* Political instability
* Fragility indicators
* Risk exposure analysis
* Vulnerability assessment

**Insights Added:**

* Pinpoints countries at risk of systemic collapse due to multi-domain weaknesses.
* Shows correlation between political instability and economic fragility.
* Identifies early warning signals for potential crises.

---

### 🌾 Food Security


images/food_security.png

Analyzes:

* Food vulnerability
* Food dependency
* Undernourishment trends
* FAO Food Price Index
* Commodity price shocks

**Insights Added:**

* Reveals countries highly exposed to global food price volatility.
* Identifies regions where food insecurity is structurally embedded.
* Tracks how global commodity shocks impact different economies unevenly.

---

### ⚡ Future Shock Index


images/future_shock_index.png

Evaluates:

* Future preparedness
* Composite resilience capacity
* Multi-domain vulnerability
* Long-term sustainability

**Insights Added:**

* Predicts which countries are most prepared for future global disruptions.
* Highlights countries with strong current performance but weak future readiness.
* Identifies resilience gaps that could become critical under climate or economic stress.

---

## 🧮 Methodology

### Data Processing Workflow

1. Data Collection
2. Data Cleaning
3. Data Validation
4. Data Normalization
5. Domain Aggregation
6. Composite Score Calculation
7. Dashboard Development
8. Insight Generation

### Normalization Formula

```text
0.01 + ((Value - Min) / (Max - Min)) × 0.99
```

Inverse indicators are automatically reversed so that higher scores always indicate better resilience.

**Additional Insight:**

* Normalization ensures fair comparison across countries with vastly different scales.
* Composite scoring balances all domains to avoid bias toward any single indicator.

---

## 📈 Key Features

✅ Composite Resilience Score
✅ Country Ranking System
✅ Regional Benchmarking
✅ Domain Analysis
✅ Risk Assessment
✅ Food Security Monitoring
✅ Future Shock Evaluation
✅ Interactive Plotly Visualizations
✅ Streamlit Dashboard

**Enhanced Value:**

* Enables decision-makers to quickly identify priority areas for intervention.
* Supports policy analysis and strategic planning using data-driven evidence.

---

## 🛠️ Tech Stack

### Programming

* Python

### Libraries

* Pandas
* NumPy
* Plotly
* Streamlit
* OpenPyXL

### Data Sources

* World Bank Indicators
* FAO Food Price Index

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Global-Resilience-Index
```

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

### 3. Run the Dashboard

```bash
streamlit run Dashboard.py
```

### 4. Open the Dashboard

After running the command, Streamlit will generate a local URL similar to:

```text
http://localhost:8501
```

Open the URL in your browser.

---

## ⚠️ Dataset Requirements

This repository contains the dashboard application only.

The dashboard expects access to the **Final_Data_EXCEL** dataset directory that contains all source files used in the analysis.

Required structure:

```text
Final_Data_EXCEL/
├── Climate & Energy/
├── Digital Infrastructure/
├── Economic Fragility/
├── Food/
├── Healthcare Capacity/
└── Political Stability/
```

Before loading the dashboard:

* Ensure the dataset folder exists on your machine.
* Select or enter the correct dataset path from the Streamlit sidebar.
* Keep all Excel files in their original folders.
* Do not modify the internal folder structure.

If the dataset path is incorrect, the dashboard will not be able to load the data.

---

## 🌍 Dataset Coverage

| Metric       | Value            |
| ------------ | ---------------- |
| Countries    | 100              |
| Domains      | 6                |
| Indicators   | 15+              |
| Time Period  | 2000–2023        |
| Data Sources | World Bank & FAO |

---

## 🔍 Key Insights Generated

* Global resilience rankings across 100 countries.
* Regional resilience comparisons.
* Domain-level strengths and weaknesses.
* High-risk and vulnerable country identification.
* Food security and commodity shock analysis.
* Long-term resilience trend evaluation.
* Future shock preparedness assessment.
* Identification of structural resilience gaps across regions.
* Detection of countries with hidden vulnerabilities despite strong overall scores.
* Understanding how different domains interact to shape overall resilience.
* Insights into how global crises reshape resilience patterns over time.
