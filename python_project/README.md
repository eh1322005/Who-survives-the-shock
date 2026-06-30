# 🌍 Global Resilience Index & Predictive Analytics Platform

> Measuring, analyzing, and predicting how countries withstand economic, social, environmental, and political shocks through a comprehensive data-driven resilience framework.

---

# 📖 Project Overview

The **Global Resilience Index** is an end-to-end Data Analytics and Machine Learning project designed to evaluate, compare, and predict resilience across 100 countries from 2000 to 2023.

Using World Bank and FAO datasets, the project transforms complex socio-economic, environmental, healthcare, governance, and food security indicators into a unified resilience framework that measures how countries absorb shocks, adapt to disruptions, and recover from crises.

The project is divided into two integrated layers:

### 📊 Analytics Layer

Builds a comprehensive resilience framework, generates domain scores, calculates composite resilience scores, and delivers interactive dashboards for exploration and decision-making.

### 🤖 Predictive Layer

Uses machine learning models to predict a country's Composite Resilience Score based on its performance across six resilience domains and regional characteristics.

Together, these layers provide both descriptive and predictive insights into global resilience.

---

# 🎯 Project Objectives

* Build a comprehensive Global Resilience Framework.
* Measure resilience across multiple dimensions.
* Compare countries and regions using a unified scoring methodology.
* Identify high-risk and vulnerable countries.
* Analyze long-term resilience trends.
* Evaluate preparedness for future global shocks.
* Transform complex datasets into actionable insights.
* Predict resilience levels using machine learning.
* Support data-driven policy and strategic planning.
* Reveal structural weaknesses hidden behind traditional economic indicators.

---

# 🏗️ Resilience Framework

The framework consists of six critical resilience domains:

| Domain                    | Description                                       |
| ------------------------- | ------------------------------------------------- |
| 💻 Digital Infrastructure | Internet users and broadband accessibility        |
| 📉 Economic Fragility     | GDP growth and inflation indicators               |
| 🌾 Food Security          | Food imports and undernourishment metrics         |
| 🏥 Healthcare Capacity    | Healthcare expenditure, hospitals, and physicians |
| 🏛️ Political Stability   | Governance and political stability indicators     |
| ⚡ Climate & Energy        | Energy access, renewable energy, and emissions    |

Each domain contributes to the Composite Resilience Score and represents a key pillar of national resilience.

---

# 📂 Dataset Coverage

| Metric       | Value            |
| ------------ | ---------------- |
| Countries    | 100              |
| Years        | 2000–2023        |
| Time Span    | 23 Years         |
| Domains      | 6                |
| Indicators   | 15+              |
| Data Sources | World Bank & FAO |

---

# 🔄 Data Analytics Workflow

The project follows a complete analytics lifecycle:

1. Data Collection
2. Data Cleaning
3. Data Validation
4. Data Transformation
5. Data Integration
6. Feature Engineering
7. Data Normalization
8. Domain Score Calculation
9. Composite Score Calculation
10. Dashboard Development
11. Insight Generation
12. Predictive Modeling

---

# 🧮 Normalization Methodology

All indicators are normalized using a modified Min-Max scaling approach:

```text
0.01 + ((Value - Min) / (Max - Min)) × 0.99
```

### Why This Approach?

* Eliminates scale differences between indicators.
* Ensures fair country comparisons.
* Prevents zero-value distortions.
* Creates a unified 0.01–1 scoring system.

For inverse indicators, values are automatically reversed so that higher scores always represent stronger resilience.

---

# 📊 Dashboard Pages

## 🌐 Overview Dashboard

Provides executive-level insights including:

* Global Resilience Score
* Domain Performance Comparison
* Resilience Distribution
* Decade Analysis
* Trend Monitoring

### Key Insights

* Global resilience evolution over time.
* Impact of major crises on resilience.
* Performance gaps between leading and lagging countries.
* Domains driving resilience improvement.

---

## 🔍 Country Explorer

Allows users to:

* Explore individual countries.
* Analyze resilience scorecards.
* Compare against regional averages.
* Track resilience trends.
* Benchmark domain performance.

### Key Insights

* Hidden vulnerabilities.
* Resilience balance across domains.
* Recovery speed after shocks.

---

## 🗺️ Regional Analysis

Focuses on:

* Regional rankings.
* Regional trends.
* Domain heatmaps.
* Comparative performance.
* Improvement tracking.

### Key Insights

* Regional strengths and weaknesses.
* Structural inequalities.
* Fastest-improving regions.

---

## ⚠️ Risk & Stability Dashboard

Highlights:

* Fragile countries.
* Political instability.
* Economic vulnerability.
* Risk exposure.
* Resilience weaknesses.

### Key Insights

* Early warning signals.
* Multi-domain risk concentration.
* Governance impact on resilience.

---

## 🌾 Food Security Dashboard

Analyzes:

* Food dependency.
* Food vulnerability.
* Undernourishment.
* Food Price Index.
* Commodity shocks.

### Key Insights

* Exposure to global food crises.
* Structural food insecurity.
* Regional food resilience patterns.

---

## ⚡ Future Shock Index

Evaluates:

* Future preparedness.
* Long-term sustainability.
* Multi-domain vulnerability.
* Adaptive capacity.

### Key Insights

* Future-ready countries.
* Hidden future risks.
* Sustainability resilience gaps.

---

# 🤖 Machine Learning Layer

After calculating resilience scores, the project transitions from descriptive analytics to predictive analytics.

## Problem Statement

Can a country's Composite Resilience Score be accurately predicted using its six domain scores and regional characteristics?

---

# 🎯 ML Objective

Predict:

```text
Composite Resilience Score
```

Using:

* Digital Infrastructure Score
* Economic Fragility Score
* Food Security Score
* Healthcare Capacity Score
* Political Stability Score
* Climate & Energy Score
* Region

---

# ⚙️ Machine Learning Workflow

1. Feature Selection
2. Data Preparation
3. Encoding
4. Pipeline Construction
5. Model Training
6. Hyperparameter Tuning
7. Model Evaluation
8. Feature Importance Analysis
9. Model Deployment

---

# 🧠 Models Evaluated

The project compares multiple machine learning algorithms:

* Linear Regression
* Ridge Regression
* Lasso Regression
* ElasticNet
* Decision Tree Regressor
* Random Forest Regressor
* Extra Trees Regressor
* Gradient Boosting Regressor
* Support Vector Regressor (SVR)
* K-Nearest Neighbors Regressor

Optional Models:

* XGBoost
* LightGBM
* CatBoost

---

# 📈 Model Evaluation

Models are compared using:

* R² Score
* RMSE
* MAE
* Cross Validation

The best-performing model is selected and optimized using:

* GridSearchCV
* RandomizedSearchCV

---

# 🔍 Explainability

Model interpretability includes:

* Feature Importance Analysis
* Residual Analysis
* Prediction Diagnostics
* SHAP Analysis (Optional)

---

# 🚀 Deployment

The final trained model is deployed using Streamlit.

Users can:

* Input domain scores.
* Select region.
* Generate resilience predictions instantly.
* Explore model outputs interactively.

#

---

# 🛠️ Technology Stack

## Programming

* Python

## Data Processing

* Pandas
* NumPy
* OpenPyXL

## Visualization

* Plotly
* Streamlit

## Machine Learning

* Scikit-Learn
* XGBoost
* LightGBM
* CatBoost
* SHAP

---

# 📚 Data Sources

* World Bank Open Data
* FAO Food Price Index

---

# 🚀 How to Run

## Clone Repository

```bash
git clone <repository-url>
cd Global-Resilience-Index
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Analytics Dashboard

```bash
streamlit run Dashboard.py
```

## Run ML Prediction App

```bash
streamlit run app.py
```

## CLI Prediction

```bash
python predict.py \
--digital 0.60 \
--economic 0.50 \
--food 0.70 \
--healthcare 0.65 \
--political 0.55 \
--climate 0.60 \
--region "Europe & Central Asia"
```

---

# 🌍 Key Outcomes

✅ Global Resilience Framework

✅ Composite Resilience Score

✅ Country Ranking System

✅ Regional Benchmarking

✅ Risk Assessment Engine

✅ Food Security Monitoring

✅ Future Shock Evaluation

✅ Interactive Analytics Dashboard

✅ Machine Learning Prediction System

✅ Model Deployment with Streamlit

✅ Explainable AI Analysis

✅ End-to-End Data Analytics & Data Science Pipeline

---

# 📌 Project Impact

This project demonstrates how multi-domain indicators can be integrated into a unified resilience framework to measure, compare, and predict national resilience.

By combining Data Analytics, Statistical Modeling, Machine Learning, and Interactive Visualization, the project provides a scalable approach for understanding vulnerability, preparedness, and long-term sustainability across countries.
