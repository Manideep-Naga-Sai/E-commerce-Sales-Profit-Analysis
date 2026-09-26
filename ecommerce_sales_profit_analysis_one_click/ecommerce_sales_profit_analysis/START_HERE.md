# 🚀 E-commerce Sales & Profit Analysis — One-Click Run

## Windows — easiest method

1. Open this folder.
2. Double-click **`run_project.bat`**.
3. Wait while it creates the Python environment and installs the packages.
4. The dashboard opens automatically in your browser.

You only need to do the installation the first time.

After that, simply double-click:

**`run_project.bat`**

## If Windows says Python is not recognized

Install Python 3.10 or newer and select:

**Add Python to PATH**

Then double-click `run_project.bat` again.

## Mac/Linux

Open Terminal inside this folder and run:

```bash
chmod +x run_project.sh
./run_project.sh
```

## If you use VS Code

Open the folder:

```text
ecommerce_sales_profit_analysis
```

Then either:

- double-click `run_project.bat` in the Explorer, or
- open the terminal and run `run_project.bat`

## What opens

The Streamlit dashboard contains:

- Executive Overview
- Revenue
- Profit
- Profit Margin
- Orders
- AOV
- Units Sold
- Monthly Growth
- Product Analysis
- Category Analysis
- Regional Analysis
- Customer Segment Analysis
- Interactive filters
- Revenue vs Profit analysis

## Important

The project includes a generated dataset, so you do **not** need to download a dataset before running it.

The dataset is:

```text
data/ecommerce_sales.csv
```

You can later replace that CSV with a real e-commerce dataset using the column structure documented in the main README.
