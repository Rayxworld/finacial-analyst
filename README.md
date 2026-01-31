# 💹 AI Financial Analyst (Pro Terminal)

A professional-grade, lightweight financial analysis dashboard built for speed and accuracy. This tool uses deterministic quantitative algorithms to provide real-time market insights without requiring heavy AI models or GPUs.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## ✨ Features

- **🚀 Real-Time Analysis**: Instant technical analysis using live market data.
- **📈 Technical Indicators**: Automated RSI, Bollinger Bands, SMA 50/200, and Golden/Death Cross detection.
- **📰 Sentiment Scanning**: Aggregates news headlines (via DuckDuckGo) to calculate market sentiment scores.
- **🐋 Whale Tracking**: Monitors institutional ownership and insider trading activity.
- **📊 Comparison Engine**: Compare multiple stocks (e.g., `Compare NVDA, AMD, INTC`) in a normalized performance chart.
- **📄 PDF Reports**: Generate and download professional investment memos in one click.

## 🛠️ Installation

### Option 1: Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Rayxworld/finacial-analyst.git
   cd finacial-analyst
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

### Option 2: Cloud Hosting (Free)

This app is optimized for **Streamlit Community Cloud**.
1. Fork this repo.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Deploy your repo (Main file: `app.py`).

## 🧠 How It Works

Unlike generic "Chat with Data" bots, this engine uses **Quantitative Deterministic Logic**:
- **Data Source**: `yfinance` (Yahoo Finance API) for price/volume.
- **Forecasting**: Uses `scikit-learn` Random Forest to project short-term trendlines.
- **News**: `duckduckgo-search` for real-time sentiment gathering.
- **Rendering**: `Plotly` for interactive, institutional-grade framing.

## 📂 Project Structure

- `app.py`: Main Streamlit dashboard application.
- `financial_engine.py`: Core logic for routing queries and processing data.
- `quant_utils.py`: Library of financial calculations (RSI, SMA, forecasting).
- `report_generator.py`: PDF generation engine.
- `requirements.txt`: Lightweight dependency list (CPU-only).

## 📄 License
MIT License - Free to use and modify!
