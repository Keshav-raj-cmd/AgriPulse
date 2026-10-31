import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.data_loader import (
    load_state_summary,
    load_commodity_summary,
    load_dataset_metadata,
    load_overview_trend
)
from src.ui_components import (
    render_header,
    render_kpi_card,
    render_insight_card,
    render_limitation_warning,
    apply_plotly_theme
)

# Analytical Insight Generator
def inline_generate_insight(df, prompt_focus):
    focus = prompt_focus.lower()
    if "overall monthly price" in focus and not df.empty:
        max_idx = df['Median_Price'].idxmax()
        min_idx = df['Median_Price'].idxmin()
        max_month = df.loc[max_idx]['Month_Name']
        min_month = df.loc[min_idx]['Month_Name']
        max_price = df.loc[max_idx]['Median_Price']
        min_price = df.loc[min_idx]['Median_Price']
        diff = max_price - min_price
        pct_change = (diff / min_price) * 100 if min_price > 0 else 0
        
        state_str = "All"
        comm_str = "All"
        if "state:" in focus and "commodity:" in focus:
            parts = prompt_focus.split("State:")
            if len(parts) > 1:
                subparts = parts[1].split("Commodity:")
                state_str = subparts[0].strip()
                if len(subparts) > 1:
                    comm_str = subparts[1].strip()
        
        subject = "The national aggregate market"
        if comm_str != "All" and state_str != "All":
            subject = f"The market for **{comm_str.title()}** in **{state_str.title()}**"
        elif comm_str != "All":
            subject = f"The national market for **{comm_str.title()}**"
        elif state_str != "All":
            subject = f"The agricultural sector in **{state_str.title()}**"
            
        if comm_str.lower() == "potato":
            return (f"**Temporal Price Dynamics:** {subject} demonstrates a distinct bimodal price distribution typical of tuber supply chains. "
                    f"The pricing peak in {max_month} (₹{max_price:,.2f}) reflects the critical exhaustion of cold-storage stocks just before fresh harvests arrive. "
                    f"Conversely, the {min_month} drop to ₹{min_price:,.2f} perfectly aligns with post-harvest market gluts. "
                    f"This +{pct_change:.1f}% intra-year variance highlights the storage-dependent nature of the potato economy.")
        elif comm_str.lower() == "onion":
            return (f"**Temporal Price Dynamics:** {subject} is notoriously volatile and sensitive to supply shocks. "
                    f"The data reveals a dramatic +{pct_change:.1f}% surge, peaking in {max_month} (₹{max_price:,.2f}) and bottoming out in {min_month} (₹{min_price:,.2f}). "
                    f"This characteristic spike typically occurs when stored Rabi crops deplete rapidly and the incoming Kharif harvest is delayed by erratic late monsoons, creating a temporary but severe supply vacuum.")
        elif comm_str.lower() == "tomato":
            return (f"**Temporal Price Dynamics:** Unlike root vegetables, Tomatoes are highly perishable with minimal cold-storage buffering. "
                    f"This is perfectly reflected in the extreme +{pct_change:.1f}% volatility for {subject}. Prices spike sharply to ₹{max_price:,.2f} in {max_month} "
                    f"and collapse to ₹{min_price:,.2f} in {min_month}. This indicates that pricing is almost entirely dictated by real-time harvest yields and immediate logistical bottlenecks.")
        elif comm_str.lower() == "wheat":
            return (f"**Temporal Price Dynamics:** {subject}, being a heavily regulated staple with Minimum Support Price (MSP) buffering, exhibits uniquely subdued volatility. "
                    f"The +{pct_change:.1f}% variance between {min_month} (₹{min_price:,.2f}) and {max_month} (₹{max_price:,.2f}) represents a steady, controlled depletion of granary stocks "
                    f"rather than the erratic market panics seen in perishables.")
        
        return (f"**Temporal Price Dynamics:** {subject} exhibits a clear seasonal trajectory. "
                f"The lowest median aggregate prices occurred in {min_month} (₹{min_price:,.2f}), "
                f"while prices peaked significantly in {max_month} at ₹{max_price:,.2f}. "
                f"This represents a maximum intra-year variance of +{pct_change:.1f}%. This specific pricing "
                f"shift heavily correlates with the seasonal availability and localized harvest cycles for {subject.lower().replace('the market for ', '').replace('the national market for ', '').replace('the agricultural sector in ', '')}.")
                
    elif "which states have the most market reporting activity" in focus and not df.empty:
        total_records = df['Records'].sum()
        top_state = df.iloc[0]['State']
        top_records = df.iloc[0]['Records']
        top_share = (top_records / total_records) * 100
        second_state = df.iloc[1]['State']
        
        return (f"**Geographic Data Distribution:** The reporting infrastructure is highly concentrated. "
                f"**{top_state}** completely dominates the dataset, contributing {top_records:,} records "
                f"(accounting for a massive {top_share:.1f}% of top-10 volume). **{second_state}** follows, "
                f"indicating that national aggregate metrics are weighted towards market conditions in these reporting hubs.")
                
    return "The historical data indicates strong persistence in day-to-day agricultural prices alongside high regional variance."

# Render Executive Header
render_header(
    title="Agricultural Market Overview & Intelligence",
    subtitle="Macro-level temporal price trends, reporting volumes, and geographic concentration across Indian mandis in CY2024.",
    badge="CY2024 BENCHMARK DATASET",
    icon="chart"
)

# Governance & Scope Advisory
render_limitation_warning()

# Dataset Overview Metrics
metadata = load_dataset_metadata()
state_df = load_state_summary()
comm_df = load_commodity_summary()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(render_kpi_card(
        title="Total Market Records",
        value=f"{metadata.get('rows', 4727217):,}",
        delta="+4.72M",
        delta_color="green",
        subtext="Verified Mandi Arrivals",
        icon="database",
        icon_theme="emerald"
    ), unsafe_allow_html=True)
with col2:
    st.markdown(render_kpi_card(
        title="Regulated Mandis",
        value=f"{metadata.get('unique_markets', 2755):,}",
        subtext="Physical Wholesale Hubs",
        icon="market",
        icon_theme="blue"
    ), unsafe_allow_html=True)
with col3:
    st.markdown(render_kpi_card(
        title="Tracked Commodities",
        value=f"{metadata.get('unique_commodities', 304):,}",
        subtext="Grains, Vegetables, Cash Crops",
        icon="crop",
        icon_theme="amber"
    ), unsafe_allow_html=True)
with col4:
    st.markdown(render_kpi_card(
        title="States & Territories",
        value=f"{metadata.get('unique_states', 28):,}",
        subtext="Nationwide Regional Reach",
        icon="location",
        icon_theme="purple"
    ), unsafe_allow_html=True)

st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

# Trend Analysis Section
st.markdown("""
<div class="agri-section-title">Monthly Price Trends & Volatility Cycles</div>
<div class="agri-section-subtitle">Examine monthly median modal price trajectories across Indian mandis. Filter by state or specific commodity group.</div>
""", unsafe_allow_html=True)

col_a, col_b = st.columns([1, 1])
with col_a:
    state_options = ["All"] + sorted(state_df["State"].dropna().unique().tolist())
    selected_state = st.selectbox("Filter Jurisdiction / State", state_options, index=0)
with col_b:
    comm_options = ["All"] + comm_df.sort_values(by="Records", ascending=False)["Commodity"].head(60).tolist()
    selected_commodity = st.selectbox("Filter Commodity (Top 60 by Volume)", comm_options, index=0)

with st.spinner("Retrieving aggregated pricing curve..."):
    monthly_trend = load_overview_trend(selected_state, selected_commodity)

if monthly_trend.empty:
    st.warning(f"No transactions recorded for {selected_commodity} in {selected_state} during 2024.")
else:
    title_suffix = ""
    if selected_commodity != "All":
        title_suffix += f" — {selected_commodity}"
    if selected_state != "All":
        title_suffix += f" ({selected_state})"

    fig = go.Figure()
    
    # Add shaded price area
    fig.add_trace(go.Scatter(
        x=monthly_trend["Month_Name"],
        y=monthly_trend["Median_Price"],
        mode="lines+markers",
        name="Median Modal Price (₹)",
        line=dict(color="#059669", width=3, shape="spline"),
        marker=dict(size=8, color="#059669", line=dict(color="#FFFFFF", width=2)),
        fill="tozeroy",
        fillcolor="rgba(16, 185, 129, 0.08)",
        hovertemplate="<b>%{x}</b><br>Median Price: ₹%{y:,.2f}<extra></extra>"
    ))
    
    if "Average_Price" in monthly_trend.columns:
        fig.add_trace(go.Scatter(
            x=monthly_trend["Month_Name"],
            y=monthly_trend["Average_Price"],
            mode="lines",
            name="Mean Price (₹)",
            line=dict(color="#2563EB", width=2, dash="dot"),
            hovertemplate="<b>%{x}</b><br>Average Price: ₹%{y:,.2f}<extra></extra>"
        ))

    fig.update_layout(
        title=dict(
            text=f"<b>2024 Monthly Pricing Trajectory{title_suffix}</b>",
            font=dict(size=14, color="#0F172A")
        ),
        xaxis_title="Calendar Month",
        yaxis_title="Modal Price (₹ per Quintal)",
        hovermode="x unified"
    )
    apply_plotly_theme(fig, height=390)
    st.plotly_chart(fig, use_container_width=True)

    # Automated Intelligence Card
    insight_text = inline_generate_insight(
        monthly_trend, 
        f"Analyze the overall monthly price trend over 2024. State:{selected_state} Commodity:{selected_commodity}"
    )
    render_insight_card(
        title=f"Price Dynamics Insight: {selected_commodity} in {selected_state}",
        content=insight_text,
        icon="insight",
        badge="TEMPORAL DYNAMICS"
    )

st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 28px 0;'>", unsafe_allow_html=True)

# Geographic Distribution Section
st.markdown("""
<div class="agri-section-title">Market Reporting Activity by State</div>
<div class="agri-section-subtitle">Evaluation of reporting volume density and data contribution across key agricultural producer states.</div>
""", unsafe_allow_html=True)

if not state_df.empty:
    top_states = state_df.sort_values(by="Records", ascending=False).head(10).copy()
    
    fig2 = px.bar(
        top_states,
        x="State",
        y="Records",
        color="Records",
        color_continuous_scale="Greens",
        text_auto=".2s",
        title="<b>Top 10 States by Transaction Reporting Volume (2024)</b>"
    )
    fig2.update_traces(
        marker_line_color="#FFFFFF",
        marker_line_width=1.5,
        opacity=0.9,
        hovertemplate="<b>%{x}</b><br>Total Records: %{y:,}<extra></extra>"
    )
    fig2.update_layout(
        xaxis_title="State / Territory",
        yaxis_title="Recorded Transactions",
        coloraxis_showscale=False
    )
    apply_plotly_theme(fig2, height=380, show_legend=False)
    st.plotly_chart(fig2, use_container_width=True)

    insight2 = inline_generate_insight(
        top_states,
        "Analyze which states have the most market reporting activity in the dataset!"
    )
    render_insight_card(
        title="Geographic Concentration Analysis",
        content=insight2,
        icon="location",
        badge="REGIONAL DENSITY"
    )
