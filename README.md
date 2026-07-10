# 🌍 Who Survives the Shock?

## Global Crisis & Resilience Analysis Framework

### A Multi-Domain Assessment of Economic Stability, Food Security, Healthcare Capacity, Digital Infrastructure, Climate Sustainability, and Political Stability Across 100 Countries (2000–2023)

> **When the world is tested, who stands strong?**
>
> Global crises rarely occur in isolation. Economic instability, food insecurity, healthcare challenges, climate pressures, energy vulnerability, and political instability are deeply interconnected. Understanding resilience requires looking beyond individual indicators and examining how these forces interact to shape a country's ability to withstand and recover from shocks.

This project was developed as part of the **Digital Egypt Pioneers Initiative (DEPI)** and provides a comprehensive analytical framework for measuring resilience and vulnerability across 100 countries between 2000 and 2023.

By integrating data from the **World Bank**, **FAO**, and other global development indicators, the project transforms raw data into meaningful insights that support decision-making, strategic planning, and risk assessment.

---

# 👥 Team Members

| Name             | Role         | Responsibility                    |
| ---------------- | ------------ | --------------------------------- |
| Eslam Hassan     | Team Lead    | Project Management & Data Analysis|
| Mostafa ELrkhawy | Data Analyst | Research & Data Analysis          |
| Habiba Ahmed     | Data Analyst | Research & Data Analysis          |
| Sara Mohamed     | Data Analyst | Research & Data Analysis          |
| Ann Osama        | Data Analyst | Research & Data Analysis          |
| Omar Mahmoud     | Data Analyst | Research & Data Analysis          | 

### Supervisor / Instructor

**DR\ Amal Mahmoud**

---

# 🏆 Project Highlights

- 🌍 100 Officially Tracked Countries
- 📅 24 Years of Historical Data (2000–2023)
- 📊 15+ International Development Indicators
- 🏛 Six Strategic Resilience Domains
- 🌐 Multiple Trusted Global Data Sources
- 🧮 Composite Global Resilience Index
- 🧹 Advanced Data Cleaning & Feature Engineering
- 📈 Comprehensive Exploratory Data Analysis (EDA)
- 📊 Interactive Multi-Page Streamlit Dashboard
- 🤖 Machine Learning-Based Estimated Country Explorer
- 🚀 2030 Resilience Forecasting Engine
- 🎯 Optimistic, Base & Pessimistic Scenarios
- ⚠️ Country Risk Assessment & Tier Classification
- 🌎 Regional & Global Performance Benchmarking
- 💡 Executive Insights & Strategic Recommendations

---

# 🌍 About the Project

Traditional development metrics often focus on a single dimension such as economic growth or healthcare performance.

However, resilience is multidimensional.

A country may have strong economic performance but weak healthcare systems.

Another country may have strong digital infrastructure but suffer from food insecurity.

This project was designed to analyze resilience through a holistic lens by integrating multiple domains into a unified analytical framework.

The result is a comprehensive assessment of how countries absorb shocks, adapt to challenges, and sustain long-term development.

---

# ❓ Key Question

> Which countries are merely surviving global shocks, and which are truly resilient?

This project provides a data-driven answer through a framework that evaluates resilience across economic, healthcare, food-security, climate, energy, digital, and governance dimensions.

---

# 🎯 Objectives

* Measure resilience using a multi-domain approach.
* Identify vulnerable countries and regions.
* Analyze long-term global trends.
* Detect hidden relationships between indicators.
* Evaluate preparedness for future disruptions.
* Generate actionable insights supported by statistical analysis.
* Build interactive storytelling dashboards.
* Support evidence-based decision-making.

---

# 🚀 Project Implementations

Unlike traditional analytics projects that rely on a single technology, this project was fully implemented using multiple tools, with each implementation independently covering the complete analytics lifecycle from raw data to final insights and recommendations.

| Implementation | Timeline | Scope |
|---------------|----------|--------|
| 📊 Excel | Week 1 | End-to-End Analytics Solution |
| 🗄️ SQL Data Warehouse | Week 2 | End-to-End Analytics Solution |
| 🐍 Python Analytics & Machine Learning | Week 3 | Analytics + Predictive Analytics Solution |
| 📈 Power BI Dashboard | Week 4 | End-to-End Analytics Solution |
| 📊 Tableau Storytelling | Week 5 | Interactive Analytics & Storytelling Solution |

### 📊 Excel Implementation — Week 1

* Data Cleaning
* Data Transformation
* Power Query
* Power Pivot
* KPI Development
* Dashboard Design
* Business Insights
* Recommendations

### 🗄️ SQL Implementation — Week 2

* Data Cleaning
* Data Modeling
* Galaxy Schema Design
* Data Warehousing
* Analytical Queries
* Resilience Scoring
* Risk Assessment
* Insights & Recommendations

### 🐍 Python Implementation — Week 3

- Data Cleaning & Preprocessing
- Exploratory Data Analysis (EDA)
- Statistical Analysis
- Trend & Time-Series Analysis
- Correlation Analysis
- Interactive Data Visualization
- KPI Development
- Feature Engineering
- Composite Resilience Index Construction
- Machine Learning Model Development
- Model Evaluation & Performance Comparison
- Hyperparameter Tuning
- Feature Importance Analysis
- Estimated Country Prediction
- Composite & Domain Score Prediction
- Country Tier & Risk Level Classification
- 2030 Resilience Forecasting
- Multi-Scenario Forecasting (Optimistic, Base & Pessimistic)
- Streamlit Interactive Dashboard Development
- Automated Insight Generation
- Executive Recommendations

### 📈 Power BI Implementation — Week 4

* Power Query ETL
* Data Modeling
* DAX Measures
* KPI Development
* Interactive Dashboards
* Storytelling
* Executive Insights
* Recommendations

### 📊 Tableau Implementation — Week 5

- Interactive Dashboards
- Storytelling
- KPI Visualization
- Risk Analysis
- Business Insights

Each implementation was developed independently to demonstrate how the same business problem can be solved using different analytics technologies while achieving the same objective: measuring global resilience and identifying vulnerability to future shocks.

---

# 🗂️ Data Sources

## 🌍 World Bank Indicators

* Fixed Broadband Subscriptions
* Internet Users
* GDP Growth
* Inflation
* Food Imports
* Prevalence of Undernourishment
* Health Expenditure
* Hospital Beds
* Physicians
* Political Stability
* Access to Electricity
* Access to Clean Fuel
* CO₂ Emissions
* Renewable Energy
* Electricity Consumption

## 🌾 FAO Food Index

* Food Price Index
* Dairy Index
* Cereals Index
* Oils Index
* Meat Index
* Sugar Index

---

# 🏗️ Data Model

The project follows a dimensional modeling approach using a Galaxy Schema.

## Schema

---

## Fact Tables

### Fact_Global_Indicators

Contains:

* Indicator Values
* Normalized Values
* Resilience Metrics
* Country Keys
* Indicator Keys
* Year Keys

### Fact_Food

Contains:

* Food Price Index
* Commodity Categories
* Monthly Trends
* Food Price Metrics

---

## Dimension Tables

### Dim_Country

* Country
* Region

### Dim_Year

* Year
* Decade

### Dim_Indicator

* Indicator
* Domain
* Unit

### Dim_Type

* Food Category

---

# 🧹 Data Cleaning & Transformation

### Data Integration

* Combined multiple datasets into a unified analytical structure.
* Consolidated indicators from multiple sources.

### Data Filtering

* Removed years 2024 and 2025.
* Filtered selected countries.
* Excluded Egypt and Israel.

### Data Type Conversion

* Date Conversion
* Numeric Conversion
* Text Standardization

### Date Engineering

Created:

* Year
* Month
* Decade

### Data Reshaping

* Renamed indicators.
* Applied Unpivot Transformation.
* Converted wide-format datasets into long-format analytical tables.

### Duplicate Removal

* Removed duplicate records while building dimensions.

### Surrogate Keys

Generated:

* Country_Key
* Year_Key
* Indicator_Key
* Type_Key

### Indicator Standardization

* Cleaned indicator names.
* Extracted units.
* Removed unnecessary formatting.

### Country Classification

* Africa
* Europe
* Middle East
* East Asia
* South Asia
* Central Asia
* North America
* South America
* Oceania
* Central America & Caribbean

### Indicator Classification

* Digital Infrastructure
* Economic Fragility
* Food Security
* Healthcare
* Political Stability
* Climate
* Energy

### Food Classification

* Extremely Cheap
* Very Cheap
* Cheap
* Slightly Cheap
* Below Normal
* Near Normal
* Slightly Expensive
* Moderately Expensive
* Expensive
* Very Expensive

---

# 💡 Business Insights

## Overview & Domain Insights

### Key Findings

* Europe demonstrates the strongest resilience consistency.
* Digital Infrastructure is the fastest-improving domain.
* Healthcare remains the weakest global domain.
* Political Stability has shown a declining trend since 2010.
* Regional resilience differences are structural rather than temporary.

---

## Risk & Food Insights

### Key Findings

* Inflation is one of the strongest drivers of vulnerability.
* Food insecurity amplifies socio-economic risk.
* Political instability often precedes economic fragility.
* Africa faces significant multi-domain challenges.
* The 2022 food crisis created unprecedented global pressure.

---

# 📑 Statistical Insights

### Key Findings

* Digital inequality remains structural.
* Energy poverty and food insecurity are strongly linked.
* Inflation outliers create systemic risk.
* Several indicators exhibit non-normal distributions.
* Robust statistical methods are more appropriate than traditional parametric approaches.

---

# 📈 Key Results

* Built a comprehensive Global Resilience Framework covering 100 countries.
* Integrated economic, healthcare, food security, climate & energy, digital infrastructure, and political stability indicators into a unified resilience index.
* Developed complete analytics solutions using Excel, SQL, Python, Power BI, and Tableau.
* Performed exploratory data analysis (EDA), statistical analysis, and interactive data storytelling using Python.
* Built Machine Learning models to estimate resilience scores for countries with incomplete data.
* Forecasted domain and composite resilience scores through 2030 using predictive analytics.
* Identified structural resilience gaps, regional disparities, and country-level vulnerabilities.
* Generated actionable analytical, statistical, and business insights to support decision-making.
* Created an interactive, multi-platform decision-support system for resilience assessment and future shock evaluation.

---

# 📢 Recommendations

### 🌐 Accelerate Digital Inclusion

Invest in broadband and internet infrastructure to strengthen resilience.

### 🏥 Strengthen Healthcare Systems

Expand healthcare capacity and accessibility.

### 🍽️ Improve Food Security

Reduce import dependency and diversify food supply chains.

### ⚡ Expand Sustainable Energy Access

Increase renewable energy adoption and electricity accessibility.

### ⚖️ Enhance Governance & Stability

Strengthen institutions and governance frameworks.

### 📊 Promote Data-Driven Decision Making

Use integrated resilience monitoring systems to identify emerging risks early.

---
# 🚀 Project Outcome

The final solution delivers:

✅ End-to-End Data Analytics Solution

✅ Multi-Source Data Integration

✅ Advanced Data Cleaning & Transformation

✅ Star Schema Data Warehouse Design

✅ Excel Analytics & Interactive Dashboards

✅ SQL-Based Data Modeling & Analysis

✅ Python-Based EDA & Statistical Analysis

✅ Power BI Business Intelligence Dashboard

✅ Tableau Data Visualization & Storytelling

✅ Composite Global Resilience Index

✅ Six-Domain Resilience Assessment Framework

✅ Interactive Multi-Platform Dashboards

✅ Country & Regional Benchmarking

✅ Global Risk & Vulnerability Assessment

✅ Machine Learning-Based Estimated Country Analysis

✅ Composite & Domain Score Prediction

✅ Future Resilience Forecasting (2030)

✅ Multi-Scenario Forecasting (Optimistic, Base & Pessimistic)

✅ Executive Insights & Data-Driven Recommendations
