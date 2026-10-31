import pandas as pd
import streamlit as st
import json
import joblib
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

# ---------------------------------------------------------
# Data Loaders (Cached via st.cache_data)
# ---------------------------------------------------------

@st.cache_data
def load_monthly_summary():
    return pd.read_csv("data/monthly_summary.csv")

@st.cache_data
def load_state_summary():
    return pd.read_csv("data/state_summary.csv")

@st.cache_data
def load_commodity_summary():
    return pd.read_csv("data/commodity_summary.csv")

@st.cache_data
def load_market_summary():
    return pd.read_csv("data/market_summary.csv")

@st.cache_data
def load_series_latest():
    return pd.read_parquet("data/series_latest.parquet")

@st.cache_data
def load_dataset_metadata():
    with open("metadata/dataset_metadata.json", "r") as f:
        return json.load(f)

@st.cache_data
def load_dashboard_data():
    return pd.read_parquet("data/dashboard_data.parquet")

@st.cache_data(max_entries=3)
def load_overview_trend(state="All", commodity="All"):
    """Optimized trend loader: Uses instant summary for 'All', loads only 4 columns when filtered."""
    if state == "All" and commodity == "All":
        m_df = load_monthly_summary()
        return m_df[["Month", "Month_Name", "Median_Price", "Average_Price", "Records"]]
    
    # Load only necessary 4 columns for fast sub-second filtering
    cols = ["State", "Commodity", "Arrival_Date", "Modal_Price"]
    df = pd.read_parquet("data/dashboard_data.parquet", columns=cols)
    if state != "All":
        df = df[df["State"] == state]
    if commodity != "All":
        df = df[df["Commodity"] == commodity]
        
    if df.empty:
        return pd.DataFrame()
        
    df["Month"] = pd.to_datetime(df["Arrival_Date"]).dt.month
    monthly_trend = df.groupby("Month")["Modal_Price"].agg(
        Median_Price="median",
        Average_Price="mean",
        Records="count"
    ).reset_index()
    
    month_map = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 
                 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
    monthly_trend["Month_Name"] = monthly_trend["Month"].map(month_map)
    return monthly_trend

@st.cache_data
def load_model_comparison():
    return pd.read_csv("metadata/model_comparison.csv")

@st.cache_data
def load_feature_config():
    with open("metadata/feature_config.json", "r") as f:
        return json.load(f)

# ---------------------------------------------------------
# Machine Learning Model Loaders (Cached via st.cache_resource)
# ---------------------------------------------------------
@st.cache_resource
def load_linear_model():
    model = joblib.load("models/linear_model.joblib")
    preprocessor = joblib.load("models/linear_preprocessor.joblib")
    return model, preprocessor

@st.cache_resource
def load_random_forest_model():
    model = joblib.load("models/random_forest_model.joblib")
    preprocessor = joblib.load("models/random_forest_preprocessor.joblib")
    return model, preprocessor

@st.cache_resource
def load_xgboost_model():
    model = XGBRegressor()
    model.load_model("models/xgboost_model.json")
    categories = joblib.load("models/xgboost_categories.joblib")
    return model, categories

@st.cache_resource
def load_catboost_model():
    model = CatBoostRegressor()
    model.load_model("models/catboost_model.cbm")
    return model
