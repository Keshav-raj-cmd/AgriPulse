import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from src.data_loader import load_dashboard_data
from src.ui_components import (
    render_header,
    render_kpi_card,
    render_insight_card,
    render_limitation_warning,
    apply_plotly_theme
)

def inline_generate_scatter_insight(corr_val, commodity, weather_var):
    strength = "weak"
    if abs(corr_val) > 0.2: strength = "moderate"
    if abs(corr_val) > 0.5: strength = "strong"
    
    direction = "positive" if corr_val > 0 else "negative"
    
    # Categorize crop
    comm_lower = commodity.lower()
    perishables = ['tomato', 'banana', 'green chilli', 'brinjal', 'bhindi (ladies finger)']
    tubers = ['onion', 'potato']
    grains = ['wheat', 'paddy', 'rice']
    
    crop_type = "general agricultural"
    if comm_lower in perishables: crop_type = "highly perishable"
    elif comm_lower in tubers: crop_type = "storage-dependent root/tuber"
    elif comm_lower in grains: crop_type = "staple grain"

    analysis = (
        f"**Environmental Observational Analysis:** For **{commodity}**, the statistical relationship with "
        f"**{weather_var}** demonstrates a **{strength} {direction} correlation (r = {corr_val:.3f})**. "
    )
    
    if weather_var == "avg_temp":
        if crop_type == "highly perishable":
            analysis += (
                f"As a {crop_type} crop, {commodity} is sensitive to thermal stress. Ambient heat accelerates "
                f"spoilage and can trigger localized distress sales, followed by short-term supply vacuums that spike wholesale prices."
            )
        elif crop_type == "storage-dependent root/tuber":
            analysis += (
                f"For a {crop_type} like {commodity}, prolonged elevated temperatures accelerate sprouting and rot in non-refrigerated "
                f"storage facilities, impacting secondary wholesale buffer stocks."
            )
        else:
            analysis += f"Temperature transitions mark planting and harvest progression for {commodity}, aligning with seasonal price cycles."
            
    elif weather_var == "rainfall":
        if crop_type == "highly perishable":
            analysis += (
                f"Intense precipitation events often cause localized field waterlogging and impede rural transport arteries for {commodity}, "
                f"frequently producing acute short-term price spikes in terminal consumer mandis."
            )
        elif crop_type == "storage-dependent root/tuber":
            analysis += (
                f"Rainfall during harvest or transit increases moisture content, elevating storage fungal risks and altering post-harvest supply flows."
            )
        elif crop_type == "staple grain":
            analysis += (
                f"Unseasonal rainfall during the standing grain maturation phase can degrade output grade, although central buffer reserves buffer nationwide retail pricing."
            )
        else:
            analysis += "Precipitation anomalies primarily impact physical farm-to-mandi logistics and daily arrival volumes."
            
    elif weather_var == "wind_speed":
        analysis += (
            f"Sustained elevated wind velocity typically correlates with cyclonic systems or convective storm fronts, "
            f"temporarily impeding mandi arrivals, though direct linear price determination remains subdued."
        )

    analysis += (
        "\n\n**Methodological Governance Note:** This metric reflects strictly observational co-movement. "
        "Regional weather shifts coincide with harvest calendars and seasonal consumer behavior rather than operating as independent price drivers."
    )
    return analysis

def inline_generate_timeline_insight(df, commodity, weather_var):
    price_vol = df["Modal_Price"].std() / df["Modal_Price"].mean() * 100 if df["Modal_Price"].mean() > 0 else 0
    weather_vol = df[weather_var].std() / df[weather_var].mean() * 100 if df[weather_var].mean() > 0 else 0
    
    insight = (
        f"**Timeline Volatility Analysis:** Over CY 2024, the median modal price for **{commodity}** recorded "
        f"an annualized coefficient of variation of **{price_vol:.1f}%**, while nearest-station **{weather_var}** recorded **{weather_vol:.1f}%** variability. "
        f"Temporal overlay illustrates whether seasonal monsoon or summer thermal waves coincided with macro supply inflections. "
    )
    
    if weather_var == "avg_temp":
        insight += (
            f"Noticeable thermal peaks in May-June align with seasonal pre-monsoon lulls for {commodity}, where storage drawdown "
            f"and heat-induced transport challenges frequently tighten terminal wholesale availability."
        )
    elif weather_var == "rainfall":
        insight += (
            f"The monsoon surge (July through September) typically coincides with logistical frictions in rural transit, followed by "
            f"fresh Kharif harvest inflows that stabilize market prices in early Q4."
        )
    elif weather_var == "wind_speed":
        insight += (
            f"Atmospheric wind and storm anomalies correlate with transient supply delays rather than persistent structural price shifts."
        )
        
    return insight

# Header Hero
render_header(
    title="Weather & Price Linkage Analysis",
    subtitle="Observational linkage and co-movement between nearest terrestrial meteorological metrics and wholesale commodity pricing.",
    badge="CLIMATE & LOGISTICS",
    icon="weather"
)

# Governance Advisory
render_limitation_warning()

@st.cache_data
def get_weather_data_sample():
    df = load_dashboard_data()
    return df[["Commodity", "Modal_Price", "avg_temp", "rainfall", "wind_speed", "distance_km", "Arrival_Date"]]

with st.spinner("Loading meteorological dataset..."):
    df = get_weather_data_sample()

st.sidebar.markdown("### Climate Filter Controls")
commodities = df["Commodity"].value_counts().head(50).index.tolist()
selected_comm = st.sidebar.selectbox("Select Commodity (Top 50)", commodities)

weather_var_map = {
    "avg_temp": "Mean Temperature (°C)",
    "rainfall": "Precipitation (mm)",
    "wind_speed": "Wind Speed (km/h)"
}
weather_var = st.sidebar.selectbox(
    "Meteorological Variable",
    options=["avg_temp", "rainfall", "wind_speed"],
    format_func=lambda x: weather_var_map[x]
)

# Filter for the selected commodity
filtered_df = df[df["Commodity"] == selected_comm].dropna(subset=[weather_var, "Modal_Price"]).copy()

if filtered_df.empty:
    st.warning(f"No joint price and weather observations available for {selected_comm}.")
else:
    # Sampling for efficient scatter rendering
    plot_df = filtered_df.sample(5000, random_state=42) if len(filtered_df) > 5000 else filtered_df

    # Correlation calculation
    corr = plot_df[[weather_var, "Modal_Price"]].corr().iloc[0, 1]
    mean_temp_val = filtered_df[weather_var].mean()
    mean_dist_val = filtered_df["distance_km"].mean()
    mean_price_val = filtered_df["Modal_Price"].median()

    # Weather Unit Label
    unit = "°C" if weather_var == "avg_temp" else ("mm" if weather_var == "rainfall" else "km/h")

    # KPI Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_kpi_card(
            title="Selected Commodity",
            value=f"{selected_comm}",
            subtext=f"{len(filtered_df):,} Observations",
            icon="crop",
            icon_theme="emerald"
        ), unsafe_allow_html=True)
        
    with col2:
        st.markdown(render_kpi_card(
            title=f"Mean {weather_var_map[weather_var]}",
            value=f"{mean_temp_val:.1f} {unit}",
            subtext=f"Min: {filtered_df[weather_var].min():.1f} | Max: {filtered_df[weather_var].max():.1f}",
            icon="weather",
            icon_theme="blue"
        ), unsafe_allow_html=True)
        
    with col3:
        corr_label = "Positive" if corr > 0 else "Negative"
        st.markdown(render_kpi_card(
            title="Correlation (r)",
            value=f"{corr:+.3f}",
            delta=f"{corr_label} Linkage",
            delta_color="green" if abs(corr) < 0.3 else "amber",
            subtext="Observational Correlation",
            icon="chart",
            icon_theme="purple"
        ), unsafe_allow_html=True)
        
    with col4:
        st.markdown(render_kpi_card(
            title="Station Proximity",
            value=f"{mean_dist_val:.1f} km",
            subtext="Nearest Terrestrial Station",
            icon="location",
            icon_theme="amber"
        ), unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # Scatter Plot Section
    st.markdown(f"""
    <div class="agri-section-title">{selected_comm}: Price vs. {weather_var_map[weather_var]}</div>
    <div class="agri-section-subtitle">Ordinary Least Squares (OLS) regression line superimposed on historical arrivals.</div>
    """, unsafe_allow_html=True)

    fig = px.scatter(
        plot_df,
        x=weather_var,
        y="Modal_Price",
        opacity=0.45,
        trendline="ols",
        trendline_color_override="#DC2626",
        labels={weather_var: weather_var_map[weather_var], "Modal_Price": "Modal Price (₹ per Quintal)"}
    )
    fig.update_traces(marker=dict(size=5, color="#059669"))
    apply_plotly_theme(fig, height=410, show_legend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Analytical Scatter Insight
    scatter_insight = inline_generate_scatter_insight(corr, selected_comm, weather_var)
    render_insight_card(
        title=f"Correlation Assessment: {selected_comm} & {weather_var_map[weather_var]}",
        content=scatter_insight,
        icon="insight",
        badge="CORRELATION ANALYSIS"
    )

    st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 28px 0;'>", unsafe_allow_html=True)

    # Dual-Axis Timeline Section
    st.markdown(f"""
    <div class="agri-section-title">2024 Chronological Overlay: Price & {weather_var_map[weather_var]}</div>
    <div class="agri-section-subtitle">Dual-axis chronological comparison of daily median modal prices against ambient weather patterns.</div>
    """, unsafe_allow_html=True)

    timeline_df = filtered_df.groupby("Arrival_Date").agg({
        "Modal_Price": "median",
        weather_var: "mean"
    }).reset_index().sort_values("Arrival_Date")

    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig2.add_trace(
        go.Scatter(
            x=timeline_df["Arrival_Date"],
            y=timeline_df["Modal_Price"],
            name="Median Price (₹)",
            line=dict(color="#059669", width=2.5)
        ),
        secondary_y=False
    )

    weather_line_color = "#EA580C" if weather_var == "avg_temp" else ("#2563EB" if weather_var == "rainfall" else "#7C3AED")
    fig2.add_trace(
        go.Scatter(
            x=timeline_df["Arrival_Date"],
            y=timeline_df[weather_var],
            name=f"Mean {weather_var_map[weather_var]}",
            line=dict(color=weather_line_color, width=2, dash="dot"),
            opacity=0.8
        ),
        secondary_y=True
    )

    fig2.update_layout(
        hovermode="x unified",
        xaxis_title="Date (CY 2024)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig2.update_yaxes(title_text="<b>Modal Price (₹ per Quintal)</b>", secondary_y=False, color="#059669")
    fig2.update_yaxes(title_text=f"<b>{weather_var_map[weather_var]}</b>", secondary_y=True, color=weather_line_color)

    apply_plotly_theme(fig2, height=410, show_legend=True)
    st.plotly_chart(fig2, use_container_width=True)

    # Timeline Insight Card
    timeline_insight = inline_generate_timeline_insight(timeline_df, selected_comm, weather_var)
    render_insight_card(
        title="Seasonal Timeline Dynamics & Supply Inflections",
        content=timeline_insight,
        icon="insight",
        badge="TIMELINE DYNAMICS"
    )
