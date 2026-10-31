import re
import streamlit as st
import plotly.graph_objects as go

# SVG Icon Registry (Zero emojis, 100% crisp vector graphics)
SVG_ICONS = {
    "chart": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>'
    ),
    "market": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/>'
        '<path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/>'
        '<path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4"/>'
        '<path d="M2 7h20"/></svg>'
    ),
    "crop": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/>'
        '<path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>'
    ),
    "weather": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M12 2v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="M20 12h2"/><path d="m19.07 4.93-1.41 1.41"/>'
        '<path d="M15.947 12.65a4 4 0 0 0-5.925-4.128"/>'
        '<path d="M13 22H7a5 5 0 1 1 4.9-6H13a3 3 0 0 1 0 6Z"/></svg>'
    ),
    "database": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<ellipse cx="12" cy="5" rx="9" ry="3"/>'
        '<path d="M3 5V19A9 3 0 0 0 21 19V5"/>'
        '<path d="M3 12A9 3 0 0 0 21 12"/></svg>'
    ),
    "forecast": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>'
    ),
    "benchmark": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>'
    ),
    "insight": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/>'
        '<path d="M9 18h6"/><path d="M10 22h4"/></svg>'
    ),
    "location": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>'
    ),
    "info": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>'
    ),
    "table": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M3 15h18"/><path d="M9 3v18"/><path d="M15 3v18"/></svg>'
    ),
    "pulse": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>'
    ),
    "arrow_up": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="m18 15-6-6-6 6"/></svg>'
    ),
    "arrow_down": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="m6 9 6 6 6-6"/></svg>'
    ),
    "filter": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>'
    )
}

# Aliases and backward compatibility mappings
LEGACY_ICON_MAP = {
    "\U0001f4ca": "chart",
    "\U0001f4c8": "forecast",
    "\U0001f3db\ufe0f": "market",
    "\U0001f331": "crop",
    "\U0001f33e": "crop",
    "\u26c5": "weather",
    "\U0001f50d": "database",
    "\U0001f3c6": "benchmark",
    "\U0001f4a1": "insight",
    "\U0001f4cb": "database",
    "\U0001f5fa\ufe0f": "location",
    "\U0001f310": "location",
    "\u2139\ufe0f": "info",
    "analytics": "chart",
    "trends": "forecast",
    "store": "market",
    "mandi": "market",
    "commodity": "crop",
    "climate": "weather",
    "search": "database",
    "model": "benchmark",
    "idea": "insight",
    "state": "location",
    "geo": "location",
    "help": "info"
}


def get_svg_icon(icon_name="chart", color="currentColor", size=18):
    """Retrieves an SVG string by name, converting legacy emoji calls to clean vector icons."""
    if not icon_name:
        icon_name = "chart"
    if icon_name.startswith("<svg"):
        return icon_name
    key = LEGACY_ICON_MAP.get(icon_name, icon_name.lower().strip())
    template = SVG_ICONS.get(key, SVG_ICONS["chart"])
    return template.format(color=color, size=size)


def inject_custom_css():
    """Injects high-end enterprise CSS styling into the Streamlit application."""
    css = """
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Typography & Resets */
    html, body, .stApp {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        -webkit-font-smoothing: antialiased;
        color: #0F172A;
    }

    .stMarkdown, .stText, p, label, button, input, select, textarea {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Preserve Streamlit Material Symbols Iconography */
    [data-testid="stIconMaterial"],
    [data-testid="stIconMaterial"] *,
    [data-testid*="Icon"],
    [data-testid*="Icon"] *,
    .material-symbols-rounded,
    .material-symbols-outlined,
    [class*="material-symbols"],
    div[data-testid="stSidebarNav"] [data-testid="stIconMaterial"],
    div[data-testid="stExpander"] [data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Rounded' !important;
        font-weight: normal !important;
        font-style: normal !important;
        font-feature-settings: 'liga' 1 !important;
        -webkit-font-feature-settings: 'liga' 1 !important;
        display: inline-flex !important;
        align-items: center;
        justify-content: center;
        line-height: 1 !important;
        text-transform: none !important;
        letter-spacing: normal !important;
        word-wrap: normal !important;
        white-space: nowrap !important;
        direction: ltr !important;
    }
    
    /* Code and Numbers */
    code, pre, .mono-font {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1420px !important;
    }

    /* Top Header Bar */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Sidebar Refinement */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%) !important;
        border-right: 1px solid #E2E8F0 !important;
        box-shadow: 2px 0 16px rgba(0, 0, 0, 0.02) !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.25rem !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
    }

    /* Sidebar Navigation Links */
    div[data-testid="stSidebarNav"] {
        padding-top: 0.25rem;
    }

    div[data-testid="stSidebarNav"] a {
        text-decoration: none !important;
    }

    div[data-testid="stSidebarNav"] a span:not([data-testid="stIconMaterial"]) {
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.90rem !important;
        color: #334155 !important;
    }

    div[data-testid="stSidebarNav"] a[aria-current="page"] {
        background: #ECFDF5 !important;
        border-radius: 8px !important;
        border-left: 3px solid #059669 !important;
    }

    div[data-testid="stSidebarNav"] a[aria-current="page"] span:not([data-testid="stIconMaterial"]) {
        color: #047857 !important;
        font-weight: 600 !important;
    }

    div[data-testid="stSidebarNav"] a[aria-current="page"] [data-testid="stIconMaterial"] {
        color: #047857 !important;
    }

    /* Page Hero / Banner Container */
    .agri-header-hero {
        background: linear-gradient(135deg, #F0FDF4 0%, #FFFFFF 55%, #F8FAFC 100%);
        border: 1px solid #D1FAE5;
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px -2px rgba(5, 150, 105, 0.06);
        position: relative;
        overflow: hidden;
    }

    .agri-header-hero::after {
        content: '';
        position: absolute;
        top: -40px;
        right: -40px;
        width: 160px;
        height: 160px;
        background: radial-gradient(circle, rgba(5, 150, 105, 0.08) 0%, rgba(255, 255, 255, 0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }

    .agri-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        border-radius: 9999px;
        margin-bottom: 10px;
    }

    .agri-badge-green {
        background-color: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
    }

    .agri-badge-blue {
        background-color: #EFF6FF;
        color: #1D4ED8;
        border: 1px solid #BFDBFE;
    }

    .agri-badge-purple {
        background-color: #F5F3FF;
        color: #6D28D9;
        border: 1px solid #DDD6FE;
    }

    .agri-badge-amber {
        background-color: #FFFBEB;
        color: #B45309;
        border: 1px solid #FDE68A;
    }

    .agri-hero-title {
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        margin: 0 0 6px 0 !important;
        letter-spacing: -0.025em;
        line-height: 1.25;
    }

    .agri-hero-subtitle {
        font-size: 0.95rem !important;
        color: #475569 !important;
        margin: 0 !important;
        line-height: 1.5;
    }

    /* KPI Metric Cards */
    .agri-kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
        transition: all 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .agri-kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px -4px rgba(0, 0, 0, 0.06);
        border-color: #CBD5E1;
    }

    .agri-kpi-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
    }

    .agri-kpi-title {
        font-size: 0.80rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .agri-kpi-icon-bubble {
        width: 36px;
        height: 36px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .icon-emerald { background-color: #ECFDF5; color: #059669; }
    .icon-blue { background-color: #EFF6FF; color: #2563EB; }
    .icon-purple { background-color: #F5F3FF; color: #7C3AED; }
    .icon-amber { background-color: #FFFBEB; color: #D97706; }
    .icon-rose { background-color: #FEF2F2; color: #DC2626; }
    .icon-slate { background-color: #F1F5F9; color: #475569; }

    .agri-kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0F172A;
        font-family: 'JetBrains Mono', 'Plus Jakarta Sans', monospace !important;
        letter-spacing: -0.03em;
        line-height: 1.15;
        margin-bottom: 6px;
    }

    .agri-kpi-footer {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.80rem;
        color: #64748B;
        margin-top: 4px;
    }

    .agri-delta-pill {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 2px 7px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.76rem;
    }

    .delta-up { background-color: #ECFDF5; color: #047857; }
    .delta-down { background-color: #FEF2F2; color: #B91C1C; }
    .delta-neutral { background-color: #F1F5F9; color: #475569; }

    /* Insight Card */
    .agri-insight-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #059669;
        border-radius: 12px;
        padding: 18px 22px;
        margin-top: 14px;
        margin-bottom: 14px;
        box-shadow: 0 3px 12px -2px rgba(0, 0, 0, 0.03);
    }

    .agri-insight-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
    }

    .agri-insight-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #0F172A;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .agri-insight-body {
        font-size: 0.90rem;
        line-height: 1.6;
        color: #334155;
    }

    /* Section Subheaders */
    .agri-section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 18px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .agri-section-subtitle {
        font-size: 0.88rem;
        color: #64748B;
        margin-bottom: 16px;
    }

    /* Card Containers for Content & Visuals */
    .agri-content-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
    }

    /* Standard Streamlit Metric Restyling */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
    }

    div[data-testid="stMetricLabel"] p {
        font-size: 0.80rem !important;
        font-weight: 600 !important;
        color: #64748B !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
    }

    div[data-testid="stMetricValue"] div {
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        font-size: 1.75rem !important;
    }

    /* Tabs Restyling */
    div[data-testid="stTabs"] button[role="tab"] {
        font-weight: 600 !important;
        font-size: 0.90rem !important;
        padding: 8px 18px !important;
        border-radius: 8px 8px 0 0 !important;
        color: #64748B !important;
    }

    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: #047857 !important;
        border-bottom: 3px solid #059669 !important;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02) !important;
    }

    /* Streamlit Info / Warning / Alert Restyle */
    div[data-testid="stAlert"] {
        border-radius: 10px !important;
        border-width: 1px !important;
        font-size: 0.90rem !important;
    }

    /* Dataframe Polish */
    div[data-testid="stDataFrame"] {
        border-radius: 10px !important;
        border: 1px solid #E2E8F0 !important;
        overflow: hidden !important;
    }

    /* Sidebar Branding Header */
    .sidebar-brand-box {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 14px;
        background: linear-gradient(135deg, #ECFDF5 0%, #FFFFFF 100%);
        border: 1px solid #A7F3D0;
        border-radius: 12px;
        margin-bottom: 16px;
    }

    .sidebar-brand-icon {
        width: 36px;
        height: 36px;
        background: #059669;
        color: white;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 10px rgba(5, 150, 105, 0.25);
    }

    .sidebar-brand-text {
        display: flex;
        flex-direction: column;
    }

    .sidebar-brand-title {
        font-size: 1.05rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }

    .sidebar-brand-subtitle {
        font-size: 0.72rem;
        color: #047857;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }

    /* Sidebar Status Footer */
    .sidebar-status-pill {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        background: #F1F5F9;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        font-size: 0.78rem;
        color: #475569;
        font-weight: 500;
        margin-top: 14px;
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 0 rgba(16, 185, 129, 0.4);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_header(title, subtitle, badge="ENTERPRISE INTELLIGENCE", icon="chart"):
    """Renders a polished, executive header hero card with clean SVG iconography."""
    inject_custom_css()
    svg_icon = get_svg_icon(icon, color="#047857", size=14)
    html = (
        f'<div class="agri-header-hero">'
        f'<div class="agri-badge agri-badge-green"><span>{svg_icon}</span><span>{badge}</span></div>'
        f'<h1 class="agri-hero-title">{title}</h1>'
        f'<p class="agri-hero-subtitle">{subtitle}</p>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_kpi_card(title, value, delta=None, delta_color="normal", subtext="", icon="chart", icon_theme="emerald"):
    """Generates an HTML string for a high-contrast executive KPI card with vector iconography."""
    theme_colors = {
        "emerald": "#059669",
        "blue": "#2563EB",
        "purple": "#7C3AED",
        "amber": "#D97706",
        "rose": "#DC2626",
        "slate": "#475569"
    }
    color = theme_colors.get(icon_theme, "#059669")
    svg_icon = get_svg_icon(icon, color=color, size=18)
    
    delta_html = ""
    if delta is not None:
        delta_class = "delta-neutral"
        arrow_svg = ""
        if str(delta).startswith("+") or delta_color == "green":
            delta_class = "delta-up"
            arrow_svg = SVG_ICONS["arrow_up"]
        elif str(delta).startswith("-") or delta_color == "red":
            delta_class = "delta-down"
            arrow_svg = SVG_ICONS["arrow_down"]
            
        delta_html = f'<span class="agri-delta-pill {delta_class}">{arrow_svg} <span>{delta}</span></span>'

    subtext_html = f"<span>{subtext}</span>" if subtext else ""

    html = (
        f'<div class="agri-kpi-card">'
        f'<div class="agri-kpi-header">'
        f'<span class="agri-kpi-title">{title}</span>'
        f'<div class="agri-kpi-icon-bubble icon-{icon_theme}">{svg_icon}</div>'
        f'</div>'
        f'<div class="agri-kpi-value">{value}</div>'
        f'<div class="agri-kpi-footer">{delta_html}{subtext_html}</div>'
        f'</div>'
    )
    return html


def render_insight_card(title, content, icon="insight", badge="ANALYTICAL TAKEAWAY"):
    """Renders an executive insight card with clear visual hierarchy and vector icons."""
    svg_icon = get_svg_icon(icon, color="#059669", size=18)
    
    # Process markdown inside content so it renders properly inside the raw HTML container
    formatted_content = str(content)
    formatted_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', formatted_content)
    formatted_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', formatted_content)
    formatted_content = re.sub(r'`(.+?)`', r'<code>\1</code>', formatted_content)

    html = (
        f'<div class="agri-insight-card">'
        f'<div class="agri-insight-header">'
        f'<div class="agri-insight-title"><span>{svg_icon}</span><span>{title}</span></div>'
        f'<div class="agri-badge agri-badge-green" style="margin-bottom: 0;">{badge}</div>'
        f'</div>'
        f'<div class="agri-insight-body">{formatted_content}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_limitation_warning():
    """Renders the project limitation warning in a refined corporate advisory accordion without emojis."""
    with st.expander("Scope, Nearest-Station Methodology & Governance Advisory", expanded=False):
        html = (
            '<div style="font-size: 0.88rem; line-height: 1.6; color: #334155;">'
            '<ul style="margin: 0; padding-left: 20px;">'
            '<li><strong>Calendar Year 2024 Scope:</strong> All analytical aggregates and machine learning models reflect strictly the frozen CY 2024 reporting window across Indian mandis.</li>'
            '<li><strong>Nearest-Station Weather Matching:</strong> Meteorological metrics (temperature, rainfall, wind speed) originate from the nearest available terrestrial weather station (mean distance ~35km), representing regional ambient conditions rather than direct on-site sensor recordings.</li>'
            '<li><strong>Observational Association:</strong> Statistical and weather-price correlations demonstrate historical co-movement and do not imply direct mono-causality.</li>'
            '<li><strong>Analytical Framework:</strong> This platform is designed for research, policy, and market intelligence. It does not provide individualized planting advice or speculative financial guarantees.</li>'
            '</ul>'
            '</div>'
        )
        st.markdown(html, unsafe_allow_html=True)


def render_sidebar_branding():
    """Renders a sleek brand badge in the sidebar with vector branding."""
    brand_svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" '
        'fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/>'
        '<path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>'
    )
    html = (
        f'<div class="sidebar-brand-box">'
        f'<div class="sidebar-brand-icon">{brand_svg}</div>'
        f'<div class="sidebar-brand-text">'
        f'<span class="sidebar-brand-title">AgriPulse</span>'
        f'<span class="sidebar-brand-subtitle">Market Intelligence</span>'
        f'</div>'
        f'</div>'
    )
    st.sidebar.markdown(html, unsafe_allow_html=True)


def render_sidebar_status():
    """Renders operational status badge in the sidebar footer without emojis."""
    html = (
        '<div class="sidebar-status-pill">'
        '<span class="pulse-dot"></span>'
        '<span><b>Engine Active</b> · 4.7M Records · CY2024</span>'
        '</div>'
    )
    st.sidebar.markdown(html, unsafe_allow_html=True)


def apply_plotly_theme(fig, height=430, show_legend=True):
    """Applies a clean, modern fintech/enterprise theme to Plotly figures."""
    fig.update_layout(
        font_family="Plus Jakarta Sans, Inter, sans-serif",
        font_color="#334155",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=20, r=20, t=50, b=40),
        hoverlabel=dict(
            bgcolor="#0F172A",
            font_size=12,
            font_family="JetBrains Mono, sans-serif",
            font_color="#FFFFFF",
            bordercolor="#334155"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0.7)",
            bordercolor="#E2E8F0",
            borderwidth=1,
            font=dict(size=12, color="#475569")
        ) if show_legend else dict(visible=False),
        colorway=["#059669", "#2563EB", "#D97706", "#7C3AED", "#DC2626", "#0D9488", "#4F46E5"]
    )
    fig.update_xaxes(
        gridcolor="#F1F5F9",
        zerolinecolor="#E2E8F0",
        tickfont=dict(size=11, color="#64748B"),
        title_font=dict(size=12, color="#334155", weight="bold")
    )
    fig.update_yaxes(
        gridcolor="#F1F5F9",
        zerolinecolor="#E2E8F0",
        tickfont=dict(size=11, color="#64748B"),
        title_font=dict(size=12, color="#334155", weight="bold")
    )
    return fig
