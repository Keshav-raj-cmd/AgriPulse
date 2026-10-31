import streamlit as st
import importlib
import src.data_loader
importlib.reload(src.data_loader)
import src.model_loader
importlib.reload(src.model_loader)
import src.ui_components
importlib.reload(src.ui_components)

from src.ui_components import inject_custom_css, render_sidebar_branding, render_sidebar_status

st.set_page_config(
    page_title="AgriPulse | Market Intelligence & Price Forecasting",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    inject_custom_css()
    render_sidebar_branding()
    
    pages = {
        "Market Analytics": [
            st.Page("src/pages/1_Overview.py", title="Executive Overview", icon=":material/dashboard:"),
            st.Page("src/pages/2_Market_Analysis.py", title="Mandi Market Analysis", icon=":material/storefront:"),
            st.Page("src/pages/3_Commodity_Analysis.py", title="Commodity Dynamics", icon=":material/eco:"),
            st.Page("src/pages/4_Weather_Price.py", title="Weather & Price Linkage", icon=":material/cloud_queue:"),
            st.Page("src/pages/7_Data_Explorer.py", title="Data Catalog & Explorer", icon=":material/table_chart:"),
        ],
        "Machine Learning": [
            st.Page("src/pages/5_Price_Forecast.py", title="Price Forecast Terminal", icon=":material/trending_up:"),
            st.Page("src/pages/6_Model_Performance.py", title="Model Benchmarks", icon=":material/leaderboard:"),
        ]
    }
    
    pg = st.navigation(pages)
    pg.run()
    
    render_sidebar_status()

if __name__ == "__main__":
    main()
