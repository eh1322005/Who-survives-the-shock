# 🌍 Global Resilience Analytics Project

> A comprehensive SQL analytics project that evaluates resilience, risk, food security, healthcare capacity, economic stability, and future preparedness across 100 countries between 2000 and 2023.

---

# 📖 Project Overview

The Global Resilience Analytics Project was developed to measure how countries respond to economic, political, environmental, healthcare, and food-security challenges.

Using data from the World Bank and FAO, the project integrates multiple datasets into a unified analytical model that enables country ranking, regional comparison, trend analysis, and risk assessment.

The objective is not only to store data but to transform it into actionable insights that help identify resilient countries, vulnerable regions, and long-term global patterns.

---

# 🎯 Analytical Objective

Traditional economic indicators alone cannot fully explain how resilient a country is when facing crises.

This project answers questions such as:

* Which countries are the most resilient?
* Which countries face the highest risk?
* Which regions perform best across resilience domains?
* What are the main drivers of vulnerability?
* How has resilience changed over time?
* Which countries are most prepared for future shocks?

---

# 🗂️ Data Sources

### World Bank Indicators

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

### FAO

* Food Price Index
* Dairy Index
* Cereals Index
* Oils Index
* Meat Index
* Sugar Index

---

# 🏗️ Data Architecture

The project follows a dimensional modeling approach using a Star Schema.

### Fact Tables

#### Fact_Global_Indicators

Stores all resilience indicators and calculated measures.

#### Fact_Food_Index

Stores food price index metrics across years and commodity types.

---

### Dimension Tables

#### Dim_Country

* Country Key
* Country Name
* Country Code
* Region

#### Dim_Indicator

* Indicator Code
* Indicator Name
* Domain

#### Dim_Year

* Year
* Decade

#### Dim_Type

* Commodity Type

---

# 🔄 Data Preparation

The data preparation process included:

* Data Cleaning
* Data Validation
* Country Standardization
* Region Mapping
* Missing Value Handling
* Domain Classification
* Min-Max Normalization
* Indicator Transformation

---

# 🧮 Resilience Methodology

To compare indicators with different scales, Min-Max Normalization was applied.

```text
0.01 + ((Value - Min) / (Max - Min)) × 0.99
```

For inverse indicators such as:

* Inflation
* Undernourishment
* Food Dependency

the score is reversed to ensure that higher values always indicate stronger resilience.

---

# 📊 Analytical Areas

### 🌍 Country Ranking Analysis

Ranks countries according to their composite resilience score.

Key outputs:

* Top Performing Countries
* Lowest Performing Countries
* Resilience Tiers

---

### 🗺️ Regional Analysis

Compares resilience performance across world regions.

Key outputs:

* Best Region
* Weakest Region
* Regional Ranking
* Regional Improvement

---

### 📈 Trend Analysis

Analyzes resilience changes from 2000–2023.

Key outputs:

* Global Trend
* Regional Trend
* Decade Comparison
* Growth Patterns

---

### ⚠️ Risk Analysis

Identifies vulnerable countries and regions.

Key outputs:

* High-Risk Countries
* Political Instability Analysis
* Economic Fragility Assessment
* Vulnerability Classification

---

### 🌾 Food Security Analysis

Evaluates food-related resilience.

Key outputs:

* Food Dependency
* Undernourishment
* Food Vulnerability
* Commodity Price Shocks

---

### ⚡ Future Shock Analysis

Measures preparedness for future disruptions.

Key outputs:

* Future Shock Index
* Resilience Gaps
* Long-Term Sustainability Assessment

---

# 📏 Key Measures

Examples of calculated metrics include:

* Composite Resilience Score
* Regional Resilience Score
* Domain Average Score
* Food Vulnerability Score
* Food Dependency Rate
* Risk Score
* Stability Score
* Decade Improvement Score
* Future Shock Index

---

# 💡 Key Insights

The project enables stakeholders to:

* Identify resilient countries by highlighting nations that consistently achieve high scores across economic, healthcare, environmental, and technological indicators, indicating strong overall stability and adaptability.

* Detect hidden vulnerabilities by uncovering countries that may appear stable economically but suffer from weaknesses in areas such as food security, political stability, or healthcare capacity.

* Understand regional inequalities by comparing performance across regions, revealing which areas of the world are leading in resilience and which are lagging behind due to structural challenges.

* Evaluate long-term resilience trends by analyzing how countries and regions have improved or declined over time, helping to identify patterns of growth, stagnation, or deterioration.

* Assess food-security risks by examining dependency on food imports, undernourishment levels, and exposure to global food price fluctuations, which can signal potential crises.

* Measure preparedness for future disruptions by combining multiple indicators into a Future Shock Index that reflects how well countries can withstand economic shocks, environmental changes, or global crises.

---

# 🛠️ Technologies Used

* SQL
* MySQL
* MySQL Workbench
* Dimensional Modeling
* Data Warehousing
* Analytical SQL
* Business Intelligence Concepts

---

# 📂 Repository Structure

```text
Global-Resilience-Analytics/
│
├── SQL_Project_final.sql
├── Model.mwb
├── README.md
└── schema.png
```
