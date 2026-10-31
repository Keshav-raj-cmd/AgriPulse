# Agricultural Market Price Analyser
## Enterprise Market Intelligence & Price Forecasting Platform

A production-grade agricultural market intelligence platform built with **Streamlit**, **Plotly**, and **Scikit-Learn/XGBoost/CatBoost**. Analyzes historical mandi transaction prices across India (Calendar Year 2024 benchmark) and explores relationships between market prices, commodities, geographic locations, seasonality, and meteorological indicators.

---

## 1. Project Architecture & File Structure

```
agri_market_price_analyser/
├── app.py                      # Application entrypoint & multi-page navigation
├── requirements.txt            # Python dependencies
├── README.md                   # Comprehensive project documentation
├── .gitignore                  # Git exclusion rules
├── .streamlit/
│   └── config.toml             # Streamlit theme & server configuration
├── data/                       # 2024 Mandi transaction & summary datasets
│   ├── dashboard_data.parquet  # Primary 4.7M+ record benchmark dataset
│   ├── series_latest.parquet   # Latest series-level observations
│   ├── monthly_summary.csv     # Pre-aggregated monthly macro trends
│   ├── state_summary.csv       # State-level volume & price summaries
│   ├── commodity_summary.csv   # Commodity-level volume & price summaries
│   └── market_summary.csv      # Mandi market-level summaries
├── metadata/                   # Feature configurations & benchmark records
│   ├── dataset_metadata.json   # Dataset metrics (records, mandis, commodities)
│   ├── feature_config.json     # Feature schema & encoders for ML inference
│   ├── model_comparison.csv    # Official benchmark evaluation metrics
│   ├── commodity_lookup.csv    # Canonical commodity dictionary
│   ├── location_lookup.csv     # Mandi-to-station coordinates & mapping
│   └── environment_versions.txt# Environment & package versions
├── models/                     # Serialized machine learning models & preprocessors
│   ├── linear_model.joblib     # Linear Regression estimator
│   ├── linear_preprocessor.joblib # Feature pipelines for Linear Regression
│   ├── random_forest_model.joblib # Random Forest ensemble estimator
│   ├── random_forest_preprocessor.joblib # Feature pipelines for Random Forest
│   ├── xgboost_model.json      # XGBoost regression model
│   ├── xgboost_categories.joblib # Categorical encoding for XGBoost
│   └── catboost_model.cbm      # CatBoost regression model
└── src/                        # Modular source code
    ├── __init__.py
    ├── data_loader.py          # Unified data & ML model caching/loaders
    ├── ui_components.py        # Executive styling, custom KPI cards & charts
    └── pages/                  # Application views
        ├── 1_Overview.py           # Macro trends & geographic concentration
        ├── 2_Market_Analysis.py    # Mandi-level price trajectories & distributions
        ├── 3_Commodity_Analysis.py # Commodity dynamics & regional comparisons
        ├── 4_Weather_Price.py      # Agrometeorological correlations & linkage
        ├── 5_Price_Forecast.py     # Next-day ML forecasting terminal
        ├── 6_Model_Performance.py  # Model validation & benchmark leaderboards
        └── 7_Data_Explorer.py      # High-performance catalog & filtered export
```

---

## 2. Dataset Overview

* **Temporal Scope:** Calendar Year 2024 (January 1, 2024 – December 31, 2024).
* **Record Volume:** 4,727,217 verified market-arrival observations.
* **Geographic Coverage:** 28 States & Union Territories across 2,755 regulated wholesale mandis.
* **Commodity Diversity:** 304 distinct agricultural crops across cereals, pulses, vegetables, fruits, and cash crops.
* **Meteorological Integration:** Ambient surface temperature (avg/min/max), wind speed, atmospheric pressure, and rainfall mapped to each mandi via nearest terrestrial weather stations (mean station distance ~35 km).

---

## 3. Supervised Machine Learning Benchmark

The forecasting engine targets the **next calendar day's Modal Price** for an identical `State + District + Market + Commodity + Variety + Grade` time series.

### Benchmark Validation Results

| Model | MAE (₹/Quintal) | RMSE (₹/Quintal) | R² Score | Training Samples | Training Time |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Naive Baseline (t-1)** | ₹265.21 | ₹1,078.26 | 0.9651 | — | 0.00 min |
| **Linear Regression** | ₹296.72 | ₹1,051.04 | 0.9668 | 500,000 | 0.13 min |
| **Random Forest** | ₹360.40 | ₹1,332.63 | 0.9467 | 500,000 | 0.50 min |
| **XGBoost** | ₹347.73 | ₹1,561.90 | 0.9268 | 2,393,793 | 1.36 min |
| **CatBoost** | ₹346.06 | ₹1,624.56 | 0.9208 | 2,393,793 | 2.12 min |

*Data Splits: Training (2024-01-01 to 2024-09-30), Validation (2024-10-01 to 2024-11-30), Test (2024-12-01 to 2024-12-30).*

---

## 4. Key Functional Modules

1. **Executive Overview (`1_Overview.py`):** Macro-level temporal price trends, reporting volumes, and geographic density across producer states.
2. **Mandi Market Analysis (`2_Market_Analysis.py`):** Drill-down into specific wholesale mandis, evaluating modal vs min/max price spreads and trading volume.
3. **Commodity Dynamics (`3_Commodity_Analysis.py`):** Cross-state pricing comparisons, distribution spreads, and seasonal availability curves.
4. **Weather & Price Linkage (`4_Weather_Price.py`):** Multi-variable scatter plots and correlation matrices examining relationships between ambient temperature, rainfall anomalies, and modal prices.
5. **Price Forecast Terminal (`5_Price_Forecast.py`):** Interactive next-day modal price estimator comparing ML model predictions against naive benchmark baselines.
6. **Model Benchmarks (`6_Model_Performance.py`):** Comprehensive comparative evaluation of error distributions and goodness-of-fit metrics across all algorithms.
7. **Data Catalog & Explorer (`7_Data_Explorer.py`):** High-speed multi-attribute filtering, statistical summary generation, and filtered CSV export.

---

## 5. Installation & Execution

### Prerequisites
* Python 3.10+ (tested on Python 3.11 and 3.13)
* Standard Python virtual environment

### Setup Instructions

```bash
# Clone or navigate to the project directory
cd "agri_market_price_analyser"

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt

# Launch the Streamlit application
streamlit run app.py
```

The application will be accessible at `http://localhost:8501`.

---

## 6. Analytical Advisory & Limitations

1. **CY2024 Historical Scope:** All metrics and machine learning models strictly reflect the 2024 calendar year.
2. **Nearest-Station Matching:** Meteorological features represent regional ambient conditions from terrestrial weather stations rather than on-site microclimate measurements.
3. **Observational Association:** Statistical correlations indicate historical co-movement and do not imply direct mono-causality.
4. **Decision Support:** Designed for academic research, market intelligence, and policy modeling; does not constitute speculative financial advice or guaranteed commodity quotes.
