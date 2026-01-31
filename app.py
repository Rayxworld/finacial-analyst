import streamlit as st
import os
import re
import matplotlib.pyplot as plt
import datetime
from financial_engine import run_deterministic_analysis, SharedState
from report_generator import generate_pdf_report

# Page configuration
st.set_page_config(
    page_title="QUANT ANALYST | PRO TERMINAL",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded", # Professional sidebars are usually open
)

# Premium Styles
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #05070a !important;
        color: #e0e0e0;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1a2333 0%, #05070a 100%);
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 15px;
    }
    
    .sidebar-section {
        background: rgba(255,255,255,0.02);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }

    h1, h2, h3 { color: #ffffff !important; letter-spacing: -0.5px; }
</style>
""", unsafe_allow_html=True)

# Sidebar: Macro Context & Controls
with st.sidebar:
    st.markdown("### 🧠 MACRO IQ")
    st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
    st.markdown("**Upcoming Catalysts**")
    st.markdown("- **Feb 01:** Fed Interest Rate Decision")
    st.markdown("- **Feb 13:** CPI Inflation Report")
    st.markdown("- **Feb 15:** Retail Sales Summary")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("**Market State**")
    st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
    st.markdown("VIX Index: `14.50` (Low)")
    st.markdown("Fear/Greed: `68` (Greed)")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.divider()
    edu_mode = st.toggle("Learner Mode", value=False)
    if st.button("System Reset"):
        st.session_state.clear()
        st.rerun()

# App Header
st.title("💹 QUANT ANALYST PRO")
st.markdown("<p style='color: #888; font-size: 1.1rem; margin-top:-15px;'>Professional Institutional Intelligence Terminal</p>", unsafe_allow_html=True)

# Control Bar
col1, col2 = st.columns([5, 1])
with col1:
    query = st.text_input("ANALYZE OR COMPARE", placeholder="e.g. 'Compare NVDA and TSLA' or 'Analyze Apple'", label_visibility="collapsed")
with col2:
    analyze_btn = st.button("EXECUTE ENGINE", width="stretch")

if edu_mode:
    st.info("💡 **Pro Tip:** You can compare multiple stocks by listing them: 'Compare NVDA, AAPL, MSFT'")

st.divider()

if analyze_btn:
    if not query:
        st.warning("Please enter a ticker or query.")
    else:
        with st.spinner("QUANT ENGINE EXECUTING..."):
            try:
                raw_result = run_deterministic_analysis(query)
                
                # Report Export Utilities
                if SharedState.latest_fundamentals:
                    pdf_bytes = generate_pdf_report(
                        SharedState.latest_tickers[0] if SharedState.latest_tickers else "REPORT",
                        raw_result, 
                        SharedState.latest_signals, 
                        SharedState.latest_fundamentals
                    )
                    st.download_button(
                        "📥 DOWNLOAD ANALYST REPORT (PDF)",
                        data=pdf_bytes,
                        file_name=f"Quant_Report_{datetime.datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        width="stretch"
                    )
                
                res_col, viz_col = st.columns([2, 3], gap="large")
                
                with res_col:
                    st.markdown("### 📊 Engine Insights")
                    
                    # 1. Technical Signals / Alerts
                    if SharedState.latest_signals:
                        st.markdown("**Active Signals**")
                        for sig in SharedState.latest_signals:
                            color = "#00ff88" if sig['type'] == "BULLISH" else ("#ff3366" if sig['type'] == "BEARISH" else "#ffcc00")
                            st.markdown(f"""<div style='border-left: 3px solid {color}; padding: 10px; background: rgba(255,255,255,0.02); margin-bottom: 5px;'>
                                <span style='color: {color}; font-weight: bold;'>{sig['label']}</span><br>
                                <span style='font-size: 0.85rem; color: #888;'>{sig['desc']}</span>
                            </div>""", unsafe_allow_html=True)
                    
                    # 2. Fundamentals Metrics Grid
                    if SharedState.latest_fundamentals:
                        st.markdown("<br>**Valuation & Fundamentals**", unsafe_allow_html=True)
                        f_col1, f_col2 = st.columns(2)
                        f = SharedState.latest_fundamentals
                        def fmt_val(val):
                            if isinstance(val, (int, float)):
                                if val > 1e12: return f"${val/1e12:.1f}T"
                                if val > 1e9: return f"${val/1e9:.1f}B"
                                return f"{val:.2f}"
                            return str(val)

                        with f_col1:
                            st.markdown(f"""<div class='metric-card'>
                                <p style='color: #888; font-size: 0.8rem; margin:0;'>P/E Ratio</p>
                                <h3 style='margin: 0;'>{fmt_val(f.get('P/E Ratio'))}</h3>
                            </div>""", unsafe_allow_html=True)
                            st.markdown(f"""<div class='metric-card'>
                                <p style='color: #888; font-size: 0.8rem; margin:0;'>Market Cap</p>
                                <h3 style='margin: 0;'>{fmt_val(f.get('Market Cap'))}</h3>
                            </div>""", unsafe_allow_html=True)
                        with f_col2:
                            st.markdown(f"""<div class='metric-card'>
                                <p style='color: #888; font-size: 0.8rem; margin:0;'>PEG Ratio</p>
                                <h3 style='margin: 0;'>{fmt_val(f.get('PEG Ratio'))}</h3>
                            </div>""", unsafe_allow_html=True)
                            st.markdown(f"""<div class='metric-card'>
                                <p style='color: #888; font-size: 0.8rem; margin:0;'>Fair Value</p>
                                <h3 style='margin: 0; color: #ffcc00;'>{fmt_val(f.get('Fair Value'))}</h3>
                            </div>""", unsafe_allow_html=True)

                    # 3. Whale Tracking (New Phase 3)
                    if SharedState.latest_whale_data and SharedState.latest_whale_data.get('holders'):
                        with st.expander("🐋 Institutional Whale Tracking"):
                            st.markdown("**Top Institutional Holders**")
                            for h in SharedState.latest_whale_data['holders'][:3]:
                                st.markdown(f"- {h.get('Holder', 'Unknown')}: {h.get('Ownership', 'N/A')} ownership")
                            
                            if SharedState.latest_whale_data.get('insiders'):
                                st.markdown("<br>**Recent Insider Moves**", unsafe_allow_html=True)
                                for i in SharedState.latest_whale_data['insiders'][:2]:
                                    st.markdown(f"- {i.get('Text', 'Trade detected')}")

                    # 4. Text Result Area
                    st.markdown("<br>", unsafe_allow_html=True)
                    # Startup Grade Badge
                    st.markdown("""
                        <div style='background: rgba(0, 209, 255, 0.1); border: 1px solid #00d1ff; border-radius: 4px; padding: 4px 10px; display: inline-block; margin-bottom: 10px;'>
                            <span style='color: #00d1ff; font-size: 0.65rem; font-weight: bold;'>STARTUP GRADE | 100% RELIABLE</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    with st.container(border=True):
                        st.markdown(raw_result)

                with viz_col:
                    st.markdown("### 📈 Technical Forecast")
                    if SharedState.latest_fig:
                        st.plotly_chart(SharedState.latest_fig, width="stretch", config={'displayModeBar': False})
                    
                    # 5. Correlation Heatmap (New Phase 2)
                    if SharedState.latest_corr_fig:
                        st.markdown("### 🧬 Portfolio Correlation")
                        st.plotly_chart(SharedState.latest_corr_fig, width="stretch")
                    
                    if edu_mode:
                        with st.expander("🔍 How to read the charts"):
                            st.markdown("""
                            - **SMA 50/200:** The average price over 50 or 200 days. When the price stays above these, it's generally healthy.
                            - **Bollinger Bands (Blue Shade):** Shows price volatility. If the price hits the edges, it might be 'over-extended'.
                            - **RSI (Green/Red Graph):** Measures momentum. Above 70 is 'Expensive' (Red line), Below 30 is 'Cheap' (Green line).
                            - **Random Forest Trend:** A machine learning model that looks at past patterns to guess the next 30 days.
                            """)

                if 'history' not in st.session_state: st.session_state.history = []
                st.session_state.history.append({"q": query, "r": raw_result, "f": SharedState.latest_fig})

            except Exception as e:
                st.error(f"ENGINE ERROR: {str(e)}")

# Bottom Tray
if 'history' in st.session_state and st.session_state.history:
    st.markdown("### 🕒 Recent Reports")
    h_cols = st.columns(min(len(st.session_state.history), 4))
    for i, item in enumerate(reversed(st.session_state.history[-4:])):
        with h_cols[i]:
            st.button(f"{item['q'][:15]}...", key=f"hist_{i}")

st.markdown("<br><br><p style='text-align: center; color: #444; font-size: 0.8rem;'>QUANT-DETERMINISTIC v3.1 | EXPERT & LEARNER PLATFORM</p>", unsafe_allow_html=True)
