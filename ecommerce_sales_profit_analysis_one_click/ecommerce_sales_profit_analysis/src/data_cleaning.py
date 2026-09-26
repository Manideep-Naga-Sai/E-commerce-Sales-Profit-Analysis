from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ecommerce_sales.csv"

def load_and_clean(path=DATA):
    df = pd.read_csv(path)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

    numeric_cols = [
        "Quantity", "Unit_Price", "Discount", "Sales", "Cost", "Profit"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.drop_duplicates(subset=["Order_ID"]).copy()
    df = df.dropna(subset=["Order_ID", "Order_Date", "Customer_ID", "Product_ID"])

    # Recalculate financial fields consistently.
    df["Sales"] = (df["Quantity"] * df["Unit_Price"] * (1 - df["Discount"])).round(2)
    df["Profit"] = (df["Sales"] - df["Cost"]).round(2)
    df["Profit_Margin"] = (df["Profit"] / df["Sales"].replace(0, pd.NA)).fillna(0)

    df["Year"] = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    return df

if __name__ == "__main__":
    df = load_and_clean()
    print(df.info())
    print("\nRows:", len(df))
