import streamlit as st
import pandas as pd
from src.data_loader import load_dashboard_data
from src.ui_components import (
    render_header,
    render_kpi_card,
    render_limitation_warning
)

# Header Hero
render_header(
    title="Enterprise Data Catalog & Query Explorer",
    subtitle="Granular querying and inspection across 4.72+ million cleaned CY2024 agricultural market arrivals and matched meteorological readings.",
    badge="DATA CATALOG",
    icon="database"
)

# Governance & Scope Advisory
render_limitation_warning()

with st.spinner("Retrieving centralized data catalog (4.72M records)..."):
    df = load_dashboard_data()

st.sidebar.markdown("### Granular Data Filters")
state_options = ["All"] + sorted(df["State"].dropna().unique().tolist())
state = st.sidebar.selectbox("State / Territory", state_options)

district = "All"
market = "All"
commodity = "All"

if state != "All":
    filtered_df = df[df["State"] == state]
    district_options = ["All"] + sorted(filtered_df["District"].dropna().unique().tolist())
    district = st.sidebar.selectbox("District", district_options)
    
    if district != "All":
        filtered_df = filtered_df[filtered_df["District"] == district]
        market_options = ["All"] + sorted(filtered_df["Market"].dropna().unique().tolist())
        market = st.sidebar.selectbox("Wholesale Mandi", market_options)
        
        if market != "All":
            filtered_df = filtered_df[filtered_df["Market"] == market]
            commodity_options = ["All"] + sorted(filtered_df["Commodity"].dropna().unique().tolist())
            commodity = st.sidebar.selectbox("Commodity", commodity_options)
            
            if commodity != "All":
                filtered_df = filtered_df[filtered_df["Commodity"] == commodity]
else:
    filtered_df = df

# Overview KPI Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(render_kpi_card(
        title="Filtered Records",
        value=f"{len(filtered_df):,}",
        subtext=f"Total: {len(df):,} Rows",
        icon="database",
        icon_theme="emerald"
    ), unsafe_allow_html=True)
    
with col2:
    st.markdown(render_kpi_card(
        title="Jurisdiction Scope",
        value=f"{state if state != 'All' else 'Nationwide'}",
        subtext=f"District: {district}",
        icon="location",
        icon_theme="blue"
    ), unsafe_allow_html=True)
    
with col3:
    st.markdown(render_kpi_card(
        title="Crop Selection",
        value=f"{commodity if commodity != 'All' else 'All Crops'}",
        subtext=f"Mandi: {market}",
        icon="crop",
        icon_theme="amber"
    ), unsafe_allow_html=True)
    
with col4:
    st.markdown(render_kpi_card(
        title="Schema Width",
        value=f"{len(filtered_df.columns)} Columns",
        subtext="Relational & Climate",
        icon="table",
        icon_theme="purple"
    ), unsafe_allow_html=True)

st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

# Table Section
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("""
    <div class="agri-section-title">Verified Transaction Records</div>
    <div class="agri-section-subtitle">Displaying the first 1,000 observations matching the active query criteria.</div>
    """, unsafe_allow_html=True)
with col_head2:
    # Export capability
    export_df = filtered_df.head(5000)
    csv_data = export_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Export Filtered CSV (Top 5k)",
        data=csv_data,
        file_name="agripulse_data_export.csv",
        mime="text/csv",
        use_container_width=True
    )

preview_df = filtered_df.head(1000)

st.dataframe(
    preview_df,
    use_container_width=True,
    column_config={
        "Modal_Price": st.column_config.NumberColumn("Modal Price (₹)", format="₹%,.2f"),
        "Min_Price": st.column_config.NumberColumn("Min Price (₹)", format="₹%,.2f"),
        "Max_Price": st.column_config.NumberColumn("Max Price (₹)", format="₹%,.2f"),
        "distance_km": st.column_config.NumberColumn("Station Dist (km)", format="%.1f km"),
        "avg_temp": st.column_config.NumberColumn("Mean Temp (°C)", format="%.1f °C"),
        "min_temp": st.column_config.NumberColumn("Min Temp (°C)", format="%.1f °C"),
        "max_temp": st.column_config.NumberColumn("Max Temp (°C)", format="%.1f °C"),
        "rainfall": st.column_config.NumberColumn("Rainfall (mm)", format="%.1f mm"),
        "wind_speed": st.column_config.NumberColumn("Wind (km/h)", format="%.1f km/h"),
        "air_pressure": st.column_config.NumberColumn("Pressure (hPa)", format="%.1f hPa"),
    },
    hide_index=True
)

st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 28px 0;'>", unsafe_allow_html=True)

# Schema Dictionary
with st.expander("Catalog Schema Dictionary & Field Metadata", expanded=False):
    schema_info = [
        {"Field": "State", "Type": "Categorical", "Description": "Federated Indian state or union territory jurisdiction."},
        {"Field": "District", "Type": "Categorical", "Description": "Administrative district within the state."},
        {"Field": "Market", "Type": "Categorical", "Description": "Physical regulated APMC wholesale market (mandi)."},
        {"Field": "Commodity", "Type": "Categorical", "Description": "Standardized agricultural crop classification."},
        {"Field": "Variety", "Type": "Categorical", "Description": "Sub-variety, hybrid, or commercial cultivar classification."},
        {"Field": "Grade", "Type": "Categorical", "Description": "Quality grading classification (FAQ, Medium, Large, etc.)."},
        {"Field": "Arrival_Date", "Type": "Temporal (Date)", "Description": "Calendar reporting date of wholesale transaction."},
        {"Field": "Modal_Price", "Type": "Continuous (₹)", "Description": "Primary wholesale market price per quintal (100 kg)."},
        {"Field": "Min_Price / Max_Price", "Type": "Continuous (₹)", "Description": "Daily reported boundary prices within the trading session."},
        {"Field": "nearest_station", "Type": "Categorical", "Description": "Identification code of the nearest terrestrial weather station."},
        {"Field": "distance_km", "Type": "Continuous (km)", "Description": "Geodesic Euclidean distance from the mandi centroid to the weather station."},
        {"Field": "avg_temp", "Type": "Continuous (°C)", "Description": "24-hour mean ambient surface temperature recorded at the nearest station."},
        {"Field": "rainfall", "Type": "Continuous (mm)", "Description": "Daily aggregate precipitation recorded at the nearest station."},
        {"Field": "wind_speed", "Type": "Continuous (km/h)", "Description": "Daily average surface wind velocity recorded at the station."}
    ]
    st.table(pd.DataFrame(schema_info))
