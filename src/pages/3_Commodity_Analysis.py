import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.data_loader import load_commodity_summary
from src.ui_components import (
    render_header,
    render_kpi_card,
    render_insight_card,
    render_limitation_warning,
    apply_plotly_theme
)

def inline_generate_commodity_insight(df_price):
    if df_price.empty:
        return "No commodity pricing data available."
    
    top_comm = df_price.iloc[0]['Commodity']
    top_comm_price = df_price.iloc[0]['Median_Price']
    bottom_comm = df_price.iloc[-1]['Commodity']
    bottom_price = df_price.iloc[-1]['Median_Price']
    
    insight = (
        f"**Commodity Value Disparity:** The agricultural dataset contains wide valuation variance across crop categories. "
        f"High-value commercial and specialty items such as **{top_comm}** anchor the upper band with median prices around "
        f"₹{top_comm_price:,.2f} per quintal, which is multiples higher than high-volume bulk staples (represented by "
        f"{bottom_comm} at ₹{bottom_price:,.2f} in this cohort). "
        f"This structural stratification demonstrates why an unweighted aggregate 'agricultural price index' can be misleading. "
        f"Market dynamics are strictly governed by intrinsic shelf life, perishability, processing grade, and localized consumer demand."
    )
    return insight

# Header Hero
render_header(
    title="Commodity Dynamics & Valuation Disparity",
    subtitle="Cross-crop pricing distributions, arrival volume concentration, and intra-category market spreads across Indian mandis.",
    badge="COMMODITY INTELLIGENCE",
    icon="crop"
)

# Governance & Scope Advisory
render_limitation_warning()

comm_df = load_commodity_summary()

if not comm_df.empty:
    top_vol_crop = comm_df.sort_values(by="Records", ascending=False).iloc[0]
    robust_comm = comm_df[comm_df["Records"] >= 100].sort_values(by="Median_Price", ascending=False)
    top_value_crop = robust_comm.iloc[0] if not robust_comm.empty else comm_df.iloc[0]
    widest_reach_crop = comm_df.sort_values(by="Markets", ascending=False).iloc[0]

    # KPI Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_kpi_card(
            title="Tracked Commodities",
            value=f"{len(comm_df):,}",
            subtext="Standard Agricultural Varieties",
            icon="crop",
            icon_theme="emerald"
        ), unsafe_allow_html=True)
        
    with col2:
        st.markdown(render_kpi_card(
            title="Volume Leader",
            value=f"{top_vol_crop['Commodity']}",
            subtext=f"{top_vol_crop['Records']:,} Recorded Arrivals",
            icon="database",
            icon_theme="blue"
        ), unsafe_allow_html=True)
        
    with col3:
        st.markdown(render_kpi_card(
            title="Value Benchmark",
            value=f"₹{top_value_crop['Median_Price']:,.0f}",
            subtext=f"{top_value_crop['Commodity']} (Median / Qtl)",
            icon="chart",
            icon_theme="amber"
        ), unsafe_allow_html=True)
        
    with col4:
        st.markdown(render_kpi_card(
            title="Widest Mandi Reach",
            value=f"{widest_reach_crop['Commodity']}",
            subtext=f"Traded in {widest_reach_crop['Markets']:,} Mandis",
            icon="location",
            icon_theme="purple"
        ), unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # Tabs for Focused Analysis
    tab_vol, tab_val, tab_spread = st.tabs([
        "Volume Concentration",
        "High-Value Benchmarks",
        "Price Spreads & Range"
    ])

    with tab_vol:
        st.markdown("""
        <div class="agri-section-title">Top 20 Commodities by Arrival Frequency</div>
        <div class="agri-section-subtitle">Staple crops and high-turnover produce accounting for the majority of mandi transactions.</div>
        """, unsafe_allow_html=True)
        
        top_comm_vol = comm_df.sort_values(by="Records", ascending=False).head(20)
        
        fig1 = px.bar(
            top_comm_vol,
            x="Commodity",
            y="Records",
            color="Records",
            color_continuous_scale="Greens",
            labels={"Records": "Arrival Transactions", "Commodity": "Commodity"}
        )
        fig1.update_layout(
            xaxis_title="Agricultural Commodity",
            yaxis_title="Arrival Transactions",
            coloraxis_showscale=False
        )
        apply_plotly_theme(fig1, height=400, show_legend=False)
        st.plotly_chart(fig1, use_container_width=True)

    with tab_val:
        st.markdown("""
        <div class="agri-section-title">Top 20 Commodities by Median Price (Min. 100 Transactions)</div>
        <div class="agri-section-subtitle">Commercial cash crops, pulses, and specialty spices anchoring the upper valuation curve.</div>
        """, unsafe_allow_html=True)
        
        top_comm_price = robust_comm.head(20)
        
        fig2 = px.bar(
            top_comm_price,
            x="Commodity",
            y="Median_Price",
            color="Median_Price",
            color_continuous_scale="Blues",
            labels={"Median_Price": "Median Price (₹)", "Commodity": "Commodity"}
        )
        fig2.update_layout(
            xaxis_title="Agricultural Commodity",
            yaxis_title="Median Price (₹ per Quintal)",
            coloraxis_showscale=False
        )
        apply_plotly_theme(fig2, height=400, show_legend=False)
        st.plotly_chart(fig2, use_container_width=True)

    with tab_spread:
        st.markdown("""
        <div class="agri-section-title">Price Range Bands for Top Traded Commodities</div>
        <div class="agri-section-subtitle">Comparison of Minimum, Median, and Maximum wholesale prices showing price dispersion.</div>
        """, unsafe_allow_html=True)
        
        top_10_traded = comm_df.sort_values(by="Records", ascending=False).head(12)
        
        fig_spread = go.Figure()
        fig_spread.add_trace(go.Bar(
            name="Minimum Recorded",
            x=top_10_traded["Commodity"],
            y=top_10_traded["Minimum_Price"],
            marker_color="#94A3B8"
        ))
        fig_spread.add_trace(go.Bar(
            name="Median Price",
            x=top_10_traded["Commodity"],
            y=top_10_traded["Median_Price"],
            marker_color="#059669"
        ))
        fig_spread.add_trace(go.Bar(
            name="Maximum Recorded",
            x=top_10_traded["Commodity"],
            y=top_10_traded["Maximum_Price"],
            marker_color="#2563EB"
        ))
        fig_spread.update_layout(
            barmode="group",
            xaxis_title="Top Traded Commodity",
            yaxis_title="Price (₹ per Quintal)"
        )
        apply_plotly_theme(fig_spread, height=400, show_legend=True)
        st.plotly_chart(fig_spread, use_container_width=True)

    # Analytical Insight Card
    insight_content = inline_generate_commodity_insight(top_comm_price)
    render_insight_card(
        title="Commodity Valuation & Structural Disparity Insight",
        content=insight_content,
        icon="insight",
        badge="VALUATION ARCHITECTURE"
    )

    st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 28px 0;'>", unsafe_allow_html=True)

    # Detailed Catalog
    st.markdown("""
    <div class="agri-section-title">Complete Commodity Directory</div>
    <div class="agri-section-subtitle">Searchable catalog with average, median, minimum, and maximum price points.</div>
    """, unsafe_allow_html=True)

    st.dataframe(
        comm_df,
        use_container_width=True,
        column_config={
            "Average_Price": st.column_config.NumberColumn("Average Price (₹)", format="₹%,.2f"),
            "Median_Price": st.column_config.NumberColumn("Median Price (₹)", format="₹%,.2f"),
            "Minimum_Price": st.column_config.NumberColumn("Minimum Price (₹)", format="₹%,.2f"),
            "Maximum_Price": st.column_config.NumberColumn("Maximum Price (₹)", format="₹%,.2f"),
            "Records": st.column_config.NumberColumn("Total Arrivals", format="%d"),
            "Markets": st.column_config.NumberColumn("Mandi Count", format="%d")
        },
        hide_index=True
    )
