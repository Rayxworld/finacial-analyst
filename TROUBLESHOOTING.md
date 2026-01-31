# Troubleshooting Guide: Streamlit Installation Issues

## Issue 1: "SyntaxError: source code cannot contain null bytes"

This error indicates a corrupted Streamlit executable. This can happen due to:
- Interrupted installation
- Antivirus interference
- Disk issues

### Solutions (try in order):

### Solution 1: Clear cache and reinstall
```bash
# Remove the virtual environment
rmdir /s /q .venv

# Clear uv cache
uv cache clean

# Reinstall everything
uv sync
```

### Solution 2: Use pip directly (if uv has issues)
```bash
# Create fresh virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate

# Install dependencies
pip install streamlit crewai[tools] yfinance matplotlib pandas pydantic python-dotenv

# Run the app
streamlit run app.py
```

### Solution 3: Run without virtual environment (quick test)
```bash
# Install globally (not recommended for production)
pip install streamlit crewai[tools] yfinance matplotlib pandas pydantic python-dotenv

# Run directly
streamlit run app.py
```

## Issue 2: Network/DNS Errors

If you're getting DNS errors like "os error 11002":
- Check your internet connection
- Try again in a few minutes (temporary server issue)
- Use a different DNS server (Google DNS: 8.8.8.8)
- Disable VPN if active

## Quick Start Alternative

If installations keep failing, you can run the core functionality directly:

```bash
# Just run the finance crew directly (no UI)
python -c "from finance_crew import run_financial_analysis; print(run_financial_analysis('Analyze TSLA for the last month'))"
```

## Need Help?

1. Check if Python is installed: `python --version`
2. Check if uv is installed: `uv --version`
3. Try the pip method (Solution 2) if uv continues to have issues
