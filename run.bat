@echo off
echo Starting AI Financial Analyst...

:: Check if uv is installed
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] 'uv' is not installed. Please install it first:
    echo https://github.com/astral-sh/uv
    pause
    exit /b 1
)

:: Install dependencies
echo Installing dependencies...
uv sync

:: Start Streamlit app using Python module (avoids corrupted .exe issue)
echo Starting Streamlit UI...
uv run python -m streamlit run app.py

pause

