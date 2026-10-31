import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.data_loader import load_market_summary
from src.ui_components import (
    render_header,
    render_kpi_card,
    render_insight_card,
    render_limitation_warning,
    apply_plotly_theme
)

def inline_generate_market_insight(df, state_filter):
    if df.empty:
        return "No market transaction data available for the selected criteria."
    
    top_market = df.iloc[0]['Market']
    top_market_records = df.iloc[0]['Records']
    median_price = df.iloc[0]['Median_Price']
    avg_commodities = df['Commodities'].mean()
    
    scope = "Nationally" if state_filter == "All" else f"In **{state_filter}**"
    
    insight = (
        f"**Market Concentration Analysis:** {scope}, **{top_market}** emerges as the primary trading hub "
        f"with {top_market_records:,} recorded wholesale arrivals. "
        f"Notably, trading volume and price levels operate independently: {top_market} maintains a median price of "
        f"₹{median_price:,.2f} despite its scale. "
        f"High-volume mega-mandis consistently clear high-tonnage staple crops (such as wheat, paddy, and potatoes), "
        f"which moderates aggregate median price indices. In contrast, specialized secondary mandis focusing on "
        f"cash crops or horticulture exhibit higher price floors. Active trading hubs in this cohort manage an average "
        f"of {avg_commodities:.1f} distinct agricultural commodities."
    )
    return insight

# Header Hero
render_header(
    title="Wholesale Mandi Market Intelligence",
    subtitle="Trading volume distribution, pricing disparities, and market concentration across physical wholesale agricultural mandis.",
    badge="MARKET BENCHMARKS",
    icon="market"
)

# Governance & Scope Advisory
render_limitation_warning()

market_df = load_market_summary()

if not market_df.empty:
    st.sidebar.markdown("### Market Filter Controls")
    state_options = ["All"] + sorted(market_df["State"].dropna().unique().tolist())
    state_filter = st.sidebar.selectbox("Filter Jurisdiction / State", state_options)
    
    min_records = st.sidebar.slider("Minimum Market Arrivals Threshold", min_value=10, max_value=2000, value=50, step=25)
    
    if state_filter != "All":
        filtered_df = market_df[(market_df["State"] == state_filter) & (market_df["Records"] >= min_records)]
    else:
        filtered_df = market_df[market_df["Records"] >= min_records]
        
    if filtered_df.empty:
        st.warning(f"No markets found in {state_filter} matching the minimum arrival threshold of {min_records}.")
    else:
        sorted_by_volume = filtered_df.sort_values(by="Records", ascending=False)
        top_market_row = sorted_by_volume.iloc[0]
        
        # KPI Summary Cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(render_kpi_card(
                title="Active Mandis",
                value=f"{len(filtered_df):,}",
                delta=f"{state_filter}",
                delta_color="neutral",
                subtext="Meeting Filter Criteria",
                icon="market",
                icon_theme="emerald"
            ), unsafe_allow_html=True)
            
        with col2:
            st.markdown(render_kpi_card(
                title="Primary Trading Hub",
                value=f"{top_market_row['Market']}",
                subtext=f"{top_market_row['Records']:,} Recorded Arrivals",
                icon="location",
                icon_theme="blue"
            ), unsafe_allow_html=True)
            
        with col3:
            st.markdown(render_kpi_card(
                title="Hub Median Price",
                value=f"₹{top_market_row['Median_Price']:,.0f}",
                subtext=f"Mean: ₹{top_market_row['Average_Price']:,.0f}",
                icon="chart",
                icon_theme="amber"
            ), unsafe_allow_html=True)
            
        with col4:
            st.markdown(render_kpi_card(
                title="Avg Crop Diversity",
                value=f"{filtered_df['Commodities'].mean():.1f}",
                subtext="Commodities per Mandi",
                icon="crop",
                icon_theme="purple"
            ), unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

        # Charts Section
        col_chart1, col_chart2 = st.columns([3, 2])
        
        top_20 = sorted_by_volume.head(20)
        
        with col_chart1:
            st.markdown("""
            <div class="agri-section-title">Top 20 Mandis by Recorded Arrival Volume</div>
            <div class="agri-section-subtitle">Ranked by total transaction records with median price color indexing.</div>
            """, unsafe_allow_html=True)
            
            fig = px.bar(
                top_20,
                x="Market",
                y="Records",
                color="Median_Price",
                color_continuous_scale="Viridis",
                labels={"Records": "Arrival Transactions", "Median_Price": "Median Price (₹)"},
                hover_data={"Average_Price": ":,.2f", "Commodities": True, "State": True}
            )
            fig.update_layout(
                xaxis_title="Wholesale Mandi",
                yaxis_title="Recorded Transactions",
                coloraxis_colorbar=dict(title="Median (₹)", thickness=12, len=0.7)
            )
            apply_plotly_theme(fig, height=410, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col_chart2:
            st.markdown("""
            <div class="agri-section-title">Volume vs. Median Price Distribution</div>
            <div class="agri-section-subtitle">Examining scale efficiencies and price spreads across wholesale hubs.</div>
            """, unsafe_allow_html=True)
            
            fig_scatter = px.scatter(
                top_20,
                x="Records",
                y="Median_Price",
                size="Commodities",
                color="Median_Price",
                hover_name="Market",
                color_continuous_scale="Viridis",
                labels={"Records": "Transaction Volume", "Median_Price": "Median Price (₹)"}
            )
            fig_scatter.update_layout(
                xaxis_title="Transaction Volume",
                yaxis_title="Median Price (₹ per Quintal)",
                coloraxis_showscale=False
            )
            apply_plotly_theme(fig_scatter, height=410, show_legend=False)
            st.plotly_chart(fig_scatter, use_container_width=True)

        # Analytical Insight Card
        insight_content = inline_generate_market_insight(top_20, state_filter)
        render_insight_card(
            title=f"Market Concentration & Liquidity Dynamics ({state_filter})",
            content=insight_content,
            icon="insight",
            badge="LIQUIDITY STRUCTURE"
        )

        st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 28px 0;'>", unsafe_allow_html=True)

        # Detailed Data Table
        st.markdown("""
        <div class="agri-section-title">Wholesale Mandi Performance Directory</div>
        <div class="agri-section-subtitle">Comprehensive tabular summary of wholesale mandis, arrival counts, and aggregate pricing benchmarks.</div>
        """, unsafe_allow_html=True)

        st.dataframe(
            filtered_df,
            use_container_width=True,
            column_config={
                "Average_Price": st.column_config.NumberColumn("Average Price (₹)", format="₹%,.2f"),
                "Median_Price": st.column_config.NumberColumn("Median Price (₹)", format="₹%,.2f"),
                "Minimum_Price": st.column_config.NumberColumn("Minimum Price (₹)", format="₹%,.2f"),
                "Maximum_Price": st.column_config.NumberColumn("Maximum Price (₹)", format="₹%,.2f"),
                "Records": st.column_config.NumberColumn("Total Records", format="%d"),
                "Commodities": st.column_config.NumberColumn("Commodities Traded", format="%d")
            },
            hide_index=True
        )
