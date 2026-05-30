# 🌍 Global Development Dashboard — Power BI + ML Forecasting

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=power-bi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![World Bank API](https://img.shields.io/badge/World%20Bank-API-blue?style=for-the-badge)

---

## 📌 Project Overview

A two-part data analytics and machine learning project built as part of the **MS Data Science** program at **PAF-IAST (Spring 2026)**.

**Task 3** — An interactive Power BI dashboard analyzing global economic and digital development trends for 16 countries from 1960–2023, powered by live World Bank API data.

**Task 4** — Extension of the dashboard with a **Polynomial Regression ML model** that forecasts GDP for 5 major economies over the next 30 years (2024–2053), integrated back into Power BI for interactive exploration.

> 📊 Course: Advanced Data Visualization (COMP-834) | Submitted to: Dr. Muhammad Zeeshan

---

## 🎯 Objectives

- Connect to World Bank Open Data API and import live JSON data into Power BI
- Perform full ETL pipeline: cleaning, transformation, null handling, and data modeling
- Build a star schema with 12 DAX measures and calculated columns
- Design a professional interactive dashboard with 10 KPI cards and 5 chart types
- Train a Polynomial Regression model in Python to forecast GDP for 30 years
- Integrate ML predictions back into Power BI for a unified predictive analytics dashboard

---

## 🗂️ Project Structure

```
global-development-powerbi-dashboard/
│
├── Task_3/
│   ├── Report.docx                    # Full technical report — Task 3
│
├── Task_4/
│   ├── Task_4_Technical_report.docx   # Full technical report — Task 4
│
└── README.md                          # This file
```

---

## 📡 Data Source

**World Bank Open Data API** — 3 indicators integrated:

| Indicator | API Code | Records | Time Range |
|---|---|---|---|
| Total Population | `SP.POP.TOTL` | ~17,500 | 1960–2025 |
| GDP (Current US$) | `NY.GDP.MKTP.CD` | ~17,500 | 1960–2025 |
| Internet Users (%) | `IT.NET.USER.ZS` | ~17,556 | 1960–2025 |

**16 Countries Analyzed:**
Pakistan · India · Bangladesh · Sri Lanka · Nepal · China · Japan · United States · United Kingdom · Germany · France · Brazil · Nigeria · Indonesia · Turkey · Saudi Arabia

---

## 🔧 Task 3 — Interactive Power BI Dashboard

### ETL Pipeline

**1. Data Import**
- Used Power BI's native Web Connector to connect directly to World Bank API
- `per_page=20000` parameter set to retrieve complete data in single API calls
- Three separate queries created for Population, GDP, and Internet Users

**2. Data Transformation (Power Query)**
- Renamed columns to meaningful identifiers (Country, CountryCode, Year, GDP, etc.)
- Removed regional aggregates (Arab World, European Union, etc.) using keyword filtering
- Converted Year to Whole Number; Population, GDP, InternetUsers to Decimal
- Handled nulls: Fill Up for internet data, Fill Down for GDP/Population, zeros for remaining

**3. Data Modeling**
- Merged 3 queries into unified `Final Table` using composite key: `CountryCode + Year`
- Full Outer Join to preserve all data points
- Calculated columns: **Region** (geographic categorization) and **GDP per Capita** (GDP ÷ Population)

### DAX Measures (12 total)

| Category | Measures |
|---|---|
| Summary | Total Population (Latest), Total GDP (Latest), Average GDP per Capita, Average Internet Penetration |
| Extremum | Max GDP, Min GDP, Highest Internet Percentage |
| Country-Specific | Pakistan GDP per Capita, Latest Year GDP, Country Count |
| Analytical | GDP Growth Percentage, GDP Rank |

### Dashboard Design

**Canvas:** 2160 × 1170px | Dark theme professional aesthetic

**Left Sidebar — Interactive Slicers:**
- Country Slicer (multi-select dropdown)
- Region Slicer (geographic filter)
- Year Slicer (2000–2023 range slider)

**Row 1 — 10 KPI Cards:**
Total Population · Total GDP · Avg GDP per Capita · Max GDP · Min GDP · Pakistan GDP per Capita · Highest Internet % · Latest Year GDP · Avg Internet Penetration · Countries Analyzed

**Row 2 — Analysis Visuals:**
- 🍩 Donut Chart: Internet Penetration by Region
- 📋 Matrix Table: Country-wise Indicators (sortable)
- 💹 Scatter Plot: Wealth vs Digital Access (GDP per Capita vs Internet %)

**Row 3 — Comparative Charts:**
- 📊 Bar Chart: Top 10 Countries by GDP
- 📈 Line Chart: GDP Growth Trajectory 2000–2023

---

## 🤖 Task 4 — ML GDP Forecasting

### Model Selection

After evaluating ARIMA, XGBoost, and Linear Regression, **Polynomial Regression (degree=2)** was selected:

> With only 63 data points per country, simple models outperform complex ones. A degree-2 polynomial captures the non-linear upward GDP trend while avoiding overfitting.

### Training Code (Python / Google Colab)

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Prepare data
X = country_data[['year']].values
y = country_data['gdp'].values

# Transform features (Year + Year²)
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

# Train model
model = LinearRegression()
model.fit(X_poly, y)

# Forecast 2024–2053
future_years = np.array(range(2024, 2054)).reshape(-1, 1)
future_poly = poly.transform(future_years)
predictions = model.predict(future_poly)
```

### Model Performance

| Country | R² Score | MAE (Billion USD) | RMSE (Billion USD) |
|---|---|---|---|
| United States | 0.9034 | 765.18 | 2,372.02 |
| Bangladesh | 0.9003 | 33.13 | 39.28 |
| India | 0.8994 | 205.07 | 328.72 |
| Pakistan | 0.8233 | 22.16 | 50.16 |
| China | 0.8029 | 1,450.78 | 2,474.83 |
| **Average** | **0.8659** | **495.26** | **1,053.00** |

### 30-Year GDP Forecast (2024–2053)

| Year | Pakistan | India | China | USA | Bangladesh |
|---|---|---|---|---|---|
| 2024 | $345.5B | $3.8T | $18.5T | $27.8T | $475.2B |
| 2030 | $423.7B | $5.1T | $24.2T | $32.1T | $571.7B |
| 2040 | $571.7B | $7.1T | $33.8T | $37.9T | $723.4B |
| 2053 | $797.5B | $9.8T | $45.3T | $44.2T | $928.6B |

### 🔑 Key Findings

1. **China overtakes USA** — Around 2048–2050, China is projected to surpass the United States reaching ~$45T
2. **Pakistan 131% growth** — GDP grows from $345B (2024) to $797B (2053)
3. **India triples** — From $3.8T to $9.8T, maintaining strong emerging market momentum
4. **USA steady growth** — From $27.8T to $44.2T, consistent but slower growth
5. **Bangladesh doubles** — From $475B to $929B driven by manufacturing

### ML → Power BI Integration Pipeline

```
Power BI (Export Final Table as CSV)
        ↓
Python / Google Colab (Train Polynomial Regression + Generate Forecasts)
        ↓
Export: forecasts.csv + model_metrics.csv
        ↓
Power BI (Import CSVs → Build Predictive Analytics Dashboard)
```

---

## 📊 Key Insights

**1. Digital-Economic Correlation**
Strong positive correlation between GDP per capita and internet penetration — digital infrastructure investment and economic development are mutually reinforcing.

**2. Leapfrog Development**
Developing nations (Pakistan, Bangladesh) show rapid mobile-first internet adoption, bypassing fixed-line broadband entirely.

**3. Pakistan's Digital Opportunity**
231M population + 35.2% internet penetration = one of the world's largest untapped digital markets. At current growth rates, ~80M new internet users expected by 2030.

**4. Regional Disparity**
Europe/North America lead at 85%+ internet penetration vs South Asia/Africa at 35–45%.

**5. China's Economic Trajectory**
Most dramatic growth — $1.2T (2000) → $17.7T (2023), projected to become world's largest economy by ~2048.

---

## ⚙️ Tools & Technologies

| Tool | Purpose |
|---|---|
| Microsoft Power BI Desktop | Dashboard design, ETL, DAX measures |
| Power Query Editor | Data transformation and cleaning |
| DAX | KPI calculations and analytical measures |
| Python (Google Colab) | ML model training and forecasting |
| scikit-learn | Polynomial Regression implementation |
| pandas / numpy | Data manipulation |
| matplotlib | Model evaluation visualizations |
| World Bank Open Data API | Primary data source |

---

## 📄 Reports

- 📘 [Task 3 Full Technical Report](./Task_3/Report.docx) — Dashboard design, ETL methodology, results & analysis
- 📗 [Task 4 Full Technical Report](./Task_4/Task_4_Technical_report.docx) — ML model, forecasts, Power BI integration

---

## 👨‍💻 Authors

**Bhadur Ali** (M24F0001DS003) · **Zanab Shahzad** (M25S0061DS003)

MS Data Science · PAF-IAST · Spring 2026

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/bhadur-ali)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=flat&logo=gmail&logoColor=white)](mailto:alikhansalar5@gmail.com)
