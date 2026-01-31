import re
import yfinance as yf
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS
from quant_utils import FinancialAnalyzer

class FinancialEngine:
    """Deterministic engine for market analysis (No LLM required)."""
    
    @staticmethod
    def resolve_tickers(query):
        """Extracts valid stock tickers with surgical precision, ignoring conversational query filler."""
        # 1. Map common names and handle typos
        mappings = {
            "nvidia": "NVDA", "nvda": "NVDA",
            "apple": "AAPL", "aapl": "AAPL",
            "tesla": "TSLA", "tsla": "TSLA", "telsa": "TSLA", 
            "microsoft": "MSFT", "msft": "MSFT",
            "google": "GOOGL", "googl": "GOOGL",
            "amazon": "AMZN", "amzn": "AMZN",
            "meta": "META", "meta": "META",
            "bitcoin": "BTC-USD", "btc": "BTC-USD",
            "ethereum": "ETH-USD", "eth": "ETH-USD"
        }
        
        extracted = []
        q_lower = query.lower()
        for name, ticker in mappings.items():
            # Match word boundaries for better accuracy
            if re.search(r'\b' + name + r'\b', q_lower):
                extracted.append(ticker)

        # 2. Look for explicit uppercase tickers, excluding 2026 conversational stopwords
        STOP_WORDS = {
            "THE", "AND", "FOR", "WHAT", "NEWS", "STOCK", "QUERY", "PLOT", 
            "LAST", "MONTH", "NEXT", "DAYS", "ABOUT", "PRICE", "TREND", "INFO",
            "SHOW", "TELL", "ME", "QUANT", "THIS", "THAT", "CHECK", "ERROR", 
            "STARTUP", "HOW", "WHY", "VIEW", "DONE", "DO", "IT", "IS", "PRO",
            "USER", "TERMINAL", "PROCESS", "WHERE"
        }
        
        # Only look for standalone uppercase words 2-5 chars long
        potential_tickers = re.findall(r'\b([A-Z]{2,5})\b', query)
        
        for t in potential_tickers:
            if t not in STOP_WORDS:
                extracted.append(t)
        
        # Return unique list
        return list(set(extracted))
    
    @staticmethod
    def get_sentiment(ticker):
        """Fetches news and calculates a simple sentiment score (-1 to 1)."""
        score = 0
        news_count = 0
        headlines = []
        
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(f"{ticker} stock price news sentiment", max_results=5))
                for r in results:
                    text = (r['title'] + " " + r['body']).lower()
                    headlines.append(r['title'])
                    
                    # Very simple keyword sentiment (Local, no LLM)
                    pos = ["bullish", "growth", "buy", "up", "high", "positive", "beat", "profit"]
                    neg = ["bearish", "fall", "sell", "down", "low", "negative", "miss", "loss"]
                    
                    for p in pos:
                        if p in text: score += 1
                    for n in neg:
                        if n in text: score -= 1
                    news_count += 1
            
            final_sentiment = max(-1, min(1, score / (news_count * 2) if news_count > 0 else 0))
            return final_sentiment, headlines
        except:
            return 0, ["News currently unavailable"]

    @staticmethod
    def run_analysis(query):
        """Main entry point for the No-LLM pipeline."""
        tickers = FinancialEngine.resolve_tickers(query)
        SharedState.latest_tickers = tickers
        
        if not tickers:
            return "I couldn't find a valid stock ticker in your query. Please provide a symbol (e.g., AAPL) or a company name (e.g., Nvidia).", None

        if len(tickers) > 1:
            # Comparison Mode
            return FinancialEngine.run_comparison_pipeline(tickers)
        else:
            # Single Analysis Mode
            ticker = tickers[0]
            sentiment, news = FinancialEngine.get_sentiment(ticker)
            
            # Unpack the 5-tuple (Summary, Fig, Signals, Fundamentals, WhaleData)
            summary, fig, signals, fundamentals, whale_data = FinancialAnalyzer.get_analysis(ticker)
            
            # Store in shared state for UI access
            SharedState.latest_signals = signals
            SharedState.latest_fundamentals = fundamentals
            SharedState.latest_whale_data = whale_data
            SharedState.latest_corr_fig = None # Reset
            
            sentiment_label = "POSITIVE" if sentiment > 0.1 else ("NEGATIVE" if sentiment < -0.1 else "NEUTRAL")
            
            response = f"""### 🧬 QUANT REPORT: {ticker}
**Ticker:** {ticker}  
**Market Sentiment:** {sentiment_label} ({sentiment:+.2f})

**Technical Analysis:**
{summary}

**Latest Headlines:**
"""
            for h in news[:3]:
                response += f"- {h}\n"
                
            return response, fig

    @staticmethod
    def run_comparison_pipeline(tickers):
        """Handles multi-stock comparison logic."""
        response, fig = FinancialAnalyzer.get_comparison_analysis(tickers)
        
        # Phase 2: Add Correlation Heatmap
        corr_fig = FinancialAnalyzer.get_correlation_heatmap(tickers)
        SharedState.latest_corr_fig = corr_fig
        
        # Reset signals/fundamentals for multi-view to avoid confusion
        SharedState.latest_signals = []
        SharedState.latest_fundamentals = {}
        SharedState.latest_whale_data = {}
        
        return response, fig

class SharedState:
    latest_fig = None
    latest_signals = []
    latest_fundamentals = {}
    latest_whale_data = {}
    latest_corr_fig = None
    latest_tickers = []

def run_deterministic_analysis(query):
    SharedState.latest_fig = None
    SharedState.latest_signals = []
    SharedState.latest_fundamentals = {}
    SharedState.latest_whale_data = {}
    SharedState.latest_corr_fig = None
    
    response, fig = FinancialEngine.run_analysis(query)
    SharedState.latest_fig = fig
    return response

if __name__ == "__main__":
    res = run_deterministic_analysis("Tell me about Tesla")
    print(res)
