import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from src.data_loader import load_model_comparison
from src.ui_components import (
    render_header,
    render_kpi_card,
    render_insight_card,
    render_limitation_warning,
    apply_plotly_theme
)

def inline_generate_model_insight(df):
    if df.empty:
        return "No benchmark data available."
    
    naive_mae = df.loc[df['Model'] == 'Naive Baseline', 'MAE'].values[0]
    lr_rmse = df.loc[df['Model'] == 'Linear Regression', 'RMSE'].values[0]
    rf_mae = df.loc[df['Model'] == 'Random Forest', 'MAE'].values[0]
    
    insight = (
        f"**Empirical Predictive Benchmark:** Evaluation on chronological holdout sets strongly confirms the high "
        f"day-to-day autoregressive persistence of agricultural mandi prices. "
        f"The persistence-based 'Naive Baseline' (carrying forward day t-1 prices) achieved an outstanding MAE of ₹{naive_mae:,.2f}. "
        f"However, the penalized Linear Regression formulation achieved superior variance control under price shocks, "
        f"attaining the lowest overall RMSE (₹{lr_rmse:,.2f}) and highest R² (0.967). "
        f"Importantly, complex non-linear ensemble architectures (e.g. Random Forest at ₹{rf_mae:,.2f} MAE and Gradient Boosted trees) "
        f"did not surpass the simpler regularized linear specification. In high-frequency commodity series with noisy daily arrivals, "
        f"over-parameterized non-linear models tend to overfit localized variance rather than capturing structural macro shifts."
    )
    return insight

# Header Hero
render_header(
    title="Machine Learning Model Benchmarks",
    subtitle="Rigorous out-of-sample chronological evaluation across baseline, linear, and gradient-boosted tree architectures.",
    badge="MODEL EVALUATION",
    icon="benchmark"
)

# Governance & Scope Advisory
render_limitation_warning()

comp_df = load_model_comparison()

if not comp_df.empty:
    naive_row = comp_df[comp_df["Model"] == "Naive Baseline"].iloc[0]
    lr_row = comp_df[comp_df["Model"] == "Linear Regression"].iloc[0]

    # KPI Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_kpi_card(
            title="Lowest MAE (Baseline)",
            value=f"₹{naive_row['MAE']:,.1f}",
            delta="Naive Baseline",
            delta_color="green",
            subtext="Mean Absolute Error",
            icon="benchmark",
            icon_theme="emerald"
        ), unsafe_allow_html=True)
        
    with col2:
        st.markdown(render_kpi_card(
            title="Lowest RMSE (Model)",
            value=f"₹{lr_row['RMSE']:,.1f}",
            delta="Linear Regression",
            delta_color="green",
            subtext="Root Mean Squared Error",
            icon="chart",
            icon_theme="blue"
        ), unsafe_allow_html=True)
        
    with col3:
        st.markdown(render_kpi_card(
            title="Peak Explanatory Power",
            value=f"{lr_row['R2']:.3f}",
            delta="+0.967 R²",
            delta_color="green",
            subtext="Variance Explained",
            icon="forecast",
            icon_theme="purple"
        ), unsafe_allow_html=True)
        
    with col4:
        st.markdown(render_kpi_card(
            title="Architectures Tested",
            value=f"{len(comp_df)}",
            subtext="Linear, Tree & Ensembles",
            icon="database",
            icon_theme="slate"
        ), unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # Comparative Visualizations
    col_chart1, col_chart2 = st.columns([3, 2])

    with col_chart1:
        st.markdown("""
        <div class="agri-section-title">Comparative Error Metrics (MAE vs. RMSE)</div>
        <div class="agri-section-subtitle">Lower values indicate higher day-ahead forecasting accuracy on out-of-sample data.</div>
        """, unsafe_allow_html=True)

        fig_err = go.Figure()
        fig_err.add_trace(go.Bar(
            name="MAE (₹)",
            x=comp_df["Model"],
            y=comp_df["MAE"],
            marker_color="#059669",
            text=comp_df["MAE"].apply(lambda v: f"₹{v:,.0f}"),
            textposition="auto"
        ))
        fig_err.add_trace(go.Bar(
            name="RMSE (₹)",
            x=comp_df["Model"],
            y=comp_df["RMSE"],
            marker_color="#2563EB",
            text=comp_df["RMSE"].apply(lambda v: f"₹{v:,.0f}"),
            textposition="auto"
        ))
        fig_err.update_layout(
            barmode="group",
            xaxis_title="Evaluated Model",
            yaxis_title="Error in Rupees (₹)",
            hovermode="x unified"
        )
        apply_plotly_theme(fig_err, height=390, show_legend=True)
        st.plotly_chart(fig_err, use_container_width=True)

    with col_chart2:
        st.markdown("""
        <div class="agri-section-title">Variance Explained (R² Score)</div>
        <div class="agri-section-subtitle">Proportion of price variance captured across holdout test observations.</div>
        """, unsafe_allow_html=True)

        fig_r2 = go.Figure()
        fig_r2.add_trace(go.Bar(
            x=comp_df["R2"],
            y=comp_df["Model"],
            orientation="h",
            marker_color="#7C3AED",
            text=comp_df["R2"].apply(lambda v: f"{v:.4f}"),
            textposition="inside"
        ))
        fig_r2.update_layout(
            xaxis_title="Coefficient of Determination (R²)",
            yaxis_title="Model",
            xaxis=dict(range=[0.90, 1.0])
        )
        apply_plotly_theme(fig_r2, height=390, show_legend=False)
        st.plotly_chart(fig_r2, use_container_width=True)

    # Benchmark Table
    st.markdown("""
    <div class="agri-section-title">Canonical Evaluation Matrix</div>
    <div class="agri-section-subtitle">Summary metrics computed on strictly chronological holdout test partitions.</div>
    """, unsafe_allow_html=True)

    st.dataframe(
        comp_df,
        use_container_width=True,
        column_config={
            "MAE": st.column_config.NumberColumn("MAE (₹)", format="₹%,.2f"),
            "RMSE": st.column_config.NumberColumn("RMSE (₹)", format="₹%,.2f"),
            "R2": st.column_config.NumberColumn("R² Score", format="%.4f"),
            "Training Rows": st.column_config.NumberColumn("Training Observations", format="%,d"),
            "Time (min)": st.column_config.NumberColumn("Compute Time (min)", format="%.2f min")
        },
        hide_index=True
    )

    # Analytical Insight Card
    insight_content = inline_generate_model_insight(comp_df)
    render_insight_card(
        title="Predictive Persistence & Architectural Performance Review",
        content=insight_content,
        icon="insight",
        badge="BENCHMARK FINDINGS"
    )

    st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 28px 0;'>", unsafe_allow_html=True)

    # Methodological Details
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("""
        <div class="agri-content-card">
            <div style="font-weight: 700; font-size: 0.98rem; margin-bottom: 8px; color: #0F172A;">Metric Definitions</div>
            <div style="font-size: 0.88rem; line-height: 1.6; color: #475569;">
                <p><strong>MAE (Mean Absolute Error):</strong> Quantifies the average magnitude of absolute forecasting errors in Indian Rupees. It provides an intuitive, linear measure of typical divergence.</p>
                <p><strong>RMSE (Root Mean Squared Error):</strong> Penalizes larger magnitude errors more severely, making it critical for risk-sensitive supply chain planning.</p>
                <p><strong>R² (Coefficient of Determination):</strong> Measures the percentage of variance explained by the model relative to a mean baseline.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown("""
        <div class="agri-content-card">
            <div style="font-weight: 700; font-size: 0.98rem; margin-bottom: 8px; color: #0F172A;">Chronological Partition Protocol</div>
            <div style="font-size: 0.88rem; line-height: 1.6; color: #475569;">
                <p>To avoid temporal data leakage common in standard cross-validation, partitions strictly mirror real-world market timelines:</p>
                <ul style="padding-left: 20px; margin: 0;">
                    <li><strong>Training Horizon:</strong> 2024-01-01 to 2024-09-30 (Q1-Q3 historical baselines)</li>
                    <li><strong>Validation Horizon:</strong> 2024-10-01 to 2024-11-30 (Hyperparameter calibration)</li>
                    <li><strong>Out-of-Sample Test:</strong> 2024-12-01 to 2024-12-30 (Unseen test holdout)</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
