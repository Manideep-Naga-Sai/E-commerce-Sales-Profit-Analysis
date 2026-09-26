from pathlib import Path
import pandas as pd

from data_cleaning import load_and_clean

ROOT = Path(__file__).resolve().parents[1]

def kpis(df):
    revenue = df["Sales"].sum()
    profit = df["Profit"].sum()
    orders = df["Order_ID"].nunique()
    customers = df["Customer_ID"].nunique()
    return {
        "Revenue": revenue,
        "Profit": profit,
        "Profit Margin": profit / revenue if revenue else 0,
        "Orders": orders,
        "Customers": customers,
        "AOV": revenue / orders if orders else 0,
        "Units": df["Quantity"].sum(),
    }

def monthly(df):
    x = df.groupby("Month", as_index=False).agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique"),
    )
    x["AOV"] = x["Revenue"] / x["Orders"]
    x["Revenue_Growth"] = x["Revenue"].pct_change()
    x["Profit_Growth"] = x["Profit"].pct_change()
    return x

def product_performance(df):
    return df.groupby(["Product_ID","Product_Name"], as_index=False).agg(
        Revenue=("Sales","sum"),
        Profit=("Profit","sum"),
        Units=("Quantity","sum"),
        Orders=("Order_ID","nunique"),
        Avg_Discount=("Discount","mean"),
    ).assign(Profit_Margin=lambda x: x["Profit"] / x["Revenue"])

def category_performance(df):
    return df.groupby("Category", as_index=False).agg(
        Revenue=("Sales","sum"),
        Profit=("Profit","sum"),
        Units=("Quantity","sum"),
        Orders=("Order_ID","nunique"),
    ).assign(Profit_Margin=lambda x: x["Profit"] / x["Revenue"])

def region_performance(df):
    return df.groupby("Region", as_index=False).agg(
        Revenue=("Sales","sum"),
        Profit=("Profit","sum"),
        Orders=("Order_ID","nunique"),
    ).assign(Profit_Margin=lambda x: x["Profit"] / x["Revenue"])

def segment_performance(df):
    return df.groupby("Customer_Segment", as_index=False).agg(
        Revenue=("Sales","sum"),
        Profit=("Profit","sum"),
        Orders=("Order_ID","nunique"),
        Customers=("Customer_ID","nunique"),
    ).assign(
        AOV=lambda x: x["Revenue"] / x["Orders"],
        Revenue_per_Customer=lambda x: x["Revenue"] / x["Customers"],
        Profit_Margin=lambda x: x["Profit"] / x["Revenue"],
    )

if __name__ == "__main__":
    df = load_and_clean()
    print(kpis(df))
    print(monthly(df).tail())
