@echo off
setlocal
title E-commerce Sales & Profit Analysis

echo.
echo ==========================================
echo   E-commerce Sales & Profit Analysis
echo ==========================================
echo.

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [1/4] Creating Python environment...
    python -m venv .venv
    if errorlevel 1 (
        echo.
        echo ERROR: Python was not found.
        echo Install Python 3.10+ from https://www.python.org/downloads/
        echo Make sure "Add Python to PATH" is selected.
        pause
        exit /b 1
    )
) else (
    echo [1/4] Python environment already exists.
)

echo [2/4] Installing/updating required packages...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Could not install dependencies.
    pause
    exit /b 1
)

if not exist "data\ecommerce_sales.csv" (
    echo [3/4] Generating sample e-commerce data...
    ".venv\Scripts\python.exe" src\generate_data.py
) else (
    echo [3/4] Dataset already exists.
)

echo [4/4] Starting dashboard...
echo.
echo Your browser should open automatically.
echo To stop the dashboard, close this window or press Ctrl+C.
echo.

".venv\Scripts\python.exe" -m streamlit run app.py

pause
