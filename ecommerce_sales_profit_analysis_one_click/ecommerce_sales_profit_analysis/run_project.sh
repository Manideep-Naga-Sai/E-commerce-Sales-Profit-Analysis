#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "=========================================="
echo "  E-commerce Sales & Profit Analysis"
echo "=========================================="

if [ ! -f ".venv/bin/python" ]; then
    echo "[1/4] Creating Python environment..."
    python3 -m venv .venv
fi

echo "[2/4] Installing/updating required packages..."
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

if [ ! -f "data/ecommerce_sales.csv" ]; then
    echo "[3/4] Generating sample e-commerce data..."
    .venv/bin/python src/generate_data.py
else
    echo "[3/4] Dataset already exists."
fi

echo "[4/4] Starting dashboard..."
.venv/bin/python -m streamlit run app.py
