import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

class FinancialAnalyzer:
    """Robust utility for stock analysis and forecasting."""
    
    @staticmethod
    def get_fundamentals(ticker):
        """Fetches key valuation and fundamental metrics."""
        try:
            t = yf.Ticker(ticker)
            info = t.info
            metrics = {
                "P/E Ratio": info.get("trailingPE", "N/A"),
                "PEG Ratio": info.get("pegRatio", "N/A"),
                "Debt/Equity": info.get("debtToEquity", "N/A"),
                "Div Yield": info.get("dividendYield", "N/A"),
                "Market Cap": info.get("marketCap", "N/A"),
                "Fair Value": info.get("targetMeanPrice", "N/A")
            }
            return metrics
        except:
            return {}

    @staticmethod
    def scan_signals(df):
        """Automatically detects technical patterns and signals."""
        signals = []
        if len(df) < 200: return signals
        
        # 1. Golden/Death Cross
        last_sma50 = df['SMA50'].iloc[-1]
        last_sma200 = df['SMA200'].iloc[-1]
        prev_sma50 = df['SMA50'].iloc[-2]
        prev_sma200 = df['SMA200'].iloc[-2]
        
        if prev_sma50 < prev_sma200 and last_sma50 > last_sma200:
            signals.append({"type": "BULLISH", "label": "Golden Cross", "desc": "50-day average crossed above 200-day."})
        elif prev_sma50 > prev_sma200 and last_sma50 < last_sma200:
            signals.append({"type": "BEARISH", "label": "Death Cross", "desc": "50-day average crossed below 200-day."})
            
        # 2. RSI Signals
        last_rsi = df['RSI'].iloc[-1]
        if last_rsi > 70:
            signals.append({"type": "WARNING", "label": "Overbought (RSI)", "desc": "Market momentum may be over-extended."})
        elif last_rsi < 30:
            signals.append({"type": "BULLISH", "label": "Oversold (RSI)", "desc": "Price may be undervalued in the short term."})
            
        return signals
    
    @staticmethod
    def get_correlation_heatmap(tickers, period="1y"):
        """Calculates and renders a correlation matrix for portfolio risk."""
        try:
            data = {}
            for t in tickers:
                df = yf.download(t, period=period, threads=False, auto_adjust=True)
                if df.empty: continue
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                data[t] = df['Close'].squeeze()
            
            corr_df = pd.DataFrame(data).pct_change().corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=corr_df.values,
                x=corr_df.columns,
                y=corr_df.index,
                colorscale='RdBu',
                zmin=-1, zmax=1,
                text=np.round(corr_df.values, 2),
                texttemplate="%{text}",
                showscale=True
            ))
            
            fig.update_layout(
                title="Stock Correlation Matrix (Portfolio Risk)",
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=500
            )
            return fig
        except:
            return None

    @staticmethod
    def get_whale_data(ticker, market_cap=0):
        """Fetches institutional holders and insider transactions with smart fallback math."""
        try:
            t = yf.Ticker(ticker)
            holders_df = t.institutional_holders
            holders = []
            
            if holders_df is not None and not holders_df.empty:
                # Fuzzy Column Detection
                cols = list(holders_df.columns)
                holder_col = next((c for c in cols if any(k in c.lower() for k in ['holder', 'entity', 'institution'])), None)
                own_col = next((c for c in cols if any(k in c.lower() for k in ['%', 'pct', 'held', 'out'])), None)
                val_col = next((c for c in cols if 'value' in c.lower()), None)
                
                for _, row in holders_df.head(5).iterrows():
                    h_val = str(row[holder_col]) if holder_col else "Unknown Holder"
                    o_val = row[own_col] if own_col else None
                    
                    # Startup Grade Fallback: Calculate ownership from Value if % is missing
                    if (o_val is None or pd.isna(o_val)) and val_col and market_cap > 0:
                        try:
                            val = float(row[val_col])
                            o_val = val / market_cap
                        except: pass
                    
                    # Format ownership nicely
                    if isinstance(o_val, (float, int)) and not pd.isna(o_val):
                        o_val = f"{o_val*100:.2f}%" if o_val < 1.0 else f"{o_val:.2f}%"
                    else:
                        o_val = "N/A"
                    
                    holders.append({"Holder": h_val, "Ownership": o_val})
                
            insiders_df = t.insider_transactions
            insiders = []
            if insiders_df is not None and not insiders_df.empty:
                # Clean insider text
                for _, row in insiders_df.head(5).iterrows():
                    text = f"{row.get('Text', 'Trade')} ({row.get('Position', 'Insider')})"
                    insiders.append({"Text": text})
                
            return {"holders": holders, "insiders": insiders}
        except Exception as e:
            return {"holders": [], "insiders": [], "error": str(e)}

    def get_comparison_analysis(tickers, period="1y"):
        """Compares multiple stocks by normalizing performance to 100%."""
        try:
            fig = go.Figure()
            colors = ['#00d1ff', '#ff3366', '#ffcc00', '#00ff88', '#ffffff']
            
            summary_parts = []
            
            for i, ticker in enumerate(tickers[:5]): # Limit to 5 for clarity
                df = yf.download(ticker, period=period, threads=False, auto_adjust=True).reset_index()
                if df.empty: continue
                
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                
                # Normalize Close price to % change
                close = df['Close'].squeeze()
                if isinstance(close, pd.DataFrame): close = close.iloc[:, 0]
                
                normalized = (close / close.iloc[0]) * 100
                
                fig.add_trace(go.Scatter(
                    x=df['Date'], 
                    y=normalized, 
                    name=ticker, 
                    line=dict(color=colors[i % len(colors)], width=2)
                ))
                
                performance = normalized.iloc[-1] - 100
                summary_parts.append(f"{ticker}: {performance:+.1f}%")

            fig.update_layout(
                template='plotly_dark',
                title="Relative Performance Comparison (Normalized to 100)",
                yaxis_title="Performance (%)",
                hovermode='x unified',
                height=600,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            summary = " | ".join(summary_parts)
            return f"Comparison complete: {summary}", fig
            
        except Exception as e:
            return f"Error during comparison: {str(e)}", None

    @staticmethod
    def get_analysis(ticker, period="1y", forecast_days=30):
        try:
            # 1. Fetch Data
            df = yf.download(ticker, period=period, threads=False, auto_adjust=True).reset_index()
            if df.empty:
                return f"Error: No data found for ticker {ticker}", None
            
            # Flatten MultiIndex columns if present (common in newer yfinance)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Ensure 'Date' is a column
            if 'Date' not in df.columns:
                 df['Date'] = df.index
            
            # 2. Technical Indicators
            # Select specific Series to avoid DataFrame-to-Column assignment errors
            close_series = df['Close'].squeeze()
            if isinstance(close_series, pd.DataFrame):
                close_series = close_series.iloc[:, 0]
                
            df['SMA50'] = close_series.rolling(window=50).mean()
            df['SMA200'] = close_series.rolling(window=200).mean()
            
            # Bollinger Bands
            std = close_series.rolling(window=20).std()
            df['BB_Upper'] = df['SMA50'] + (std * 2)
            df['BB_Lower'] = df['SMA50'] - (std * 2)
            
            # RSI Calculation
            delta = close_series.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            # 3. Random Forest Forecast
            df['Target'] = close_series.shift(-1)
            train_df = df.dropna().copy()
            
            X = np.arange(len(train_df)).reshape(-1, 1)
            y = train_df['Target'].values
            
            from sklearn.ensemble import RandomForestRegressor
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X, y)
            
            # Current trend for visualization
            df['Trendline'] = model.predict(np.arange(len(df)).reshape(-1, 1))
            
            # Future projection
            last_idx = len(df) - 1
            future_indices = np.arange(last_idx, last_idx + forecast_days).reshape(-1, 1)
            future_preds = model.predict(future_indices).flatten()
            
            last_date = df['Date'].max()
            future_dates = [last_date + timedelta(days=i) for i in range(1, forecast_days + 1)]
            forecast_df = pd.DataFrame({'Date': future_dates, 'Forecast': future_preds})
            
            # 4. Visualization
            fig = make_subplots(
                rows=3, cols=1, 
                shared_xaxes=True, 
                vertical_spacing=0.03, 
                subplot_titles=(f'{ticker} Analysis', 'RSI', 'Volume'),
                row_heights=[0.6, 0.2, 0.2]
            )

            # Price Area
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close', line=dict(color='#00d1ff', width=2)), row=1, col=1)
            fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA50'], name='50 MA', line=dict(color='#ff3366', width=1)), row=1, col=1)
            
            # Bollinger Bands
            fig.add_trace(go.Scatter(x=df['Date'], y=df['BB_Upper'], name='BB Upper', line=dict(color='rgba(173, 204, 255, 0.3)', width=0), showlegend=False), row=1, col=1)
            fig.add_trace(go.Scatter(x=df['Date'], y=df['BB_Lower'], name='BB Lower', line=dict(color='rgba(173, 204, 255, 0.3)', width=0), fill='tonexty', fillcolor='rgba(173, 204, 255, 0.1)'), row=1, col=1)
            
            # Historical Trendline
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Trendline'], name='Model Trend', line=dict(color='yellow', dash='dot', width=1)), row=1, col=1)
            
            # Future Forecast
            fig.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['Forecast'], name='30D Forecast', line=dict(color='#ffcc00', dash='dash', width=2)), row=1, col=1)
            
            # RSI
            fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], name='RSI', line=dict(color='#00ff88', width=1.5)), row=2, col=1)
            fig.add_hline(y=70, line_dash="dot", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dot", line_color="green", row=2, col=1)

            # Volume
            # Safely handle Volume
            volume_series = df['Volume'].squeeze()
            if isinstance(volume_series, pd.DataFrame): volume_series = volume_series.iloc[:, 0]
            fig.add_trace(go.Bar(x=df['Date'], y=volume_series, name='Volume', marker_color='rgba(100,100,100,0.5)'), row=3, col=1)

            fig.update_layout(
                template='plotly_dark',
                hovermode='x unified',
                height=800,
                showlegend=True,
                margin=dict(l=20, r=20, t=50, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            latest_price = float(close_series.iloc[-1])
            latest_rsi = float(df['RSI'].iloc[-1])
            status = "Bearish" if latest_rsi > 70 else ("Bullish" if latest_rsi < 30 else "Neutral")
            
            summary = f"Analysis for {ticker} completed. Price: ${latest_price:.2f} | RSI: {latest_rsi:.1f} ({status})."
            
            # Phase 1: Add extra pro-data
            signals = FinancialAnalyzer.scan_signals(df)
            fundamentals = FinancialAnalyzer.get_fundamentals(ticker)
            
            # Phase 2 & 3: Whale Tracking with fallback
            m_cap = fundamentals.get("Market Cap", 0)
            if not isinstance(m_cap, (int, float)): m_cap = 0
            whale_data = FinancialAnalyzer.get_whale_data(ticker, market_cap=m_cap)
            
            return summary, fig, signals, fundamentals, whale_data
            
        except Exception as e:
            return f"Error during analysis: {str(e)}", None, [], {}
