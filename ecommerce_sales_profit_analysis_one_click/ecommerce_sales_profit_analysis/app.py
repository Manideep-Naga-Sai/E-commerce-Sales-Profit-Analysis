from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from data_cleaning import load_and_clean
from analysis import (
    kpis, monthly, product_performance,
    category_performance, region_performance, segment_performance
)

st.set_page_config(
    page_title="E-commerce Sales & Profit Analysis",
    page_icon="📊",
    layout="wide"
)

DATA = ROOT / "data" / "ecommerce_sales.csv"

@st.cache_data
def get_data():
    return load_and_clean(DATA)

df = get_data()

st.title("📊 E-commerce Sales & Profit Analysis")
st.caption("Interactive management dashboard | Python + Pandas + Plotly + Streamlit")

# Sidebar filters
st.sidebar.header("Filters")
min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()

date_range = st.sidebar.date_input(
    "Order date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

regions = st.sidebar.multiselect(
    "Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique())
)
categories = st.sidebar.multiselect(
    "Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique())
)
segments = st.sidebar.multiselect(
    "Customer Segment", sorted(df["Customer_Segment"].unique()),
    default=sorted(df["Customer_Segment"].unique())
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    d1, d2 = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    d1 = d2 = pd.to_datetime(date_range)

f = df[
    (df["Order_Date"].between(d1, d2)) &
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories)) &
    (df["Customer_Segment"].isin(segments))
].copy()

if f.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

m = kpis(f)

# KPI cards
cols = st.columns(6)
labels = [
    ("Revenue", f"₹{m['Revenue']:,.0f}"),
    ("Profit", f"₹{m['Profit']:,.0f}"),
    ("Margin", f"{m['Profit Margin']:.1%}"),
    ("Orders", f"{m['Orders']:,}"),
    ("AOV", f"₹{m['AOV']:,.0f}"),
    ("Units", f"{m['Units']:,}"),
]
for c, (label, value) in zip(cols, labels):
    c.metric(label, value)

st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "Executive Overview", "Product & Category", "Regional", "Customers"
])

with tab1:
    st.subheader("Monthly performance")
    mo = monthly(f)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=mo["Month"], y=mo["Revenue"],
        mode="lines+markers", name="Revenue"
    ))
    fig.add_trace(go.Scatter(
        x=mo["Month"], y=mo["Profit"],
        mode="lines+markers", name="Profit"
    ))
    fig.update_layout(
        xaxis_title="Month", yaxis_title="Amount (₹)",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    cat = category_performance(f).sort_values("Revenue", ascending=False)
    reg = region_performance(f).sort_values("Profit", ascending=False)

    with c1:
        st.subheader("Revenue by category")
        st.plotly_chart(
            px.bar(cat, x="Category", y="Revenue", text_auto=".2s"),
            use_container_width=True
        )

    with c2:
        st.subheader("Profit by region")
        st.plotly_chart(
            px.bar(reg, x="Region", y="Profit", text_auto=".2s"),
            use_container_width=True
        )

    st.subheader("Customer segment performance")
    seg = segment_performance(f)
    st.dataframe(
        seg.style.format({
            "Revenue": "₹{:,.0f}", "Profit": "₹{:,.0f}",
            "AOV": "₹{:,.0f}", "Revenue_per_Customer": "₹{:,.0f}",
            "Profit_Margin": "{:.1%}"
        }),
        use_container_width=True, hide_index=True
    )

with tab2:
    st.subheader("Product performance")
    prod = product_performance(f)

    c1, c2 = st.columns(2)
    with c1:
        top = prod.nlargest(10, "Revenue")
        st.plotly_chart(
            px.bar(top.sort_values("Revenue"), x="Revenue", y="Product_Name",
                   orientation="h", title="Top 10 products by revenue"),
            use_container_width=True
        )

    with c2:
        top_profit = prod.nlargest(10, "Profit")
        st.plotly_chart(
            px.bar(top_profit.sort_values("Profit"), x="Profit", y="Product_Name",
                   orientation="h", title="Top 10 products by profit"),
            use_container_width=True
        )

    st.plotly_chart(
        px.scatter(
            prod, x="Revenue", y="Profit", size="Units",
            color="Profit_Margin", hover_name="Product_Name",
            title="Revenue vs. Profit by product"
        ),
        use_container_width=True
    )

    st.subheader("Category detail")
    st.dataframe(
        category_performance(f).style.format({
            "Revenue": "₹{:,.0f}", "Profit": "₹{:,.0f}",
            "Profit_Margin": "{:.1%}"
        }),
        use_container_width=True, hide_index=True
    )

with tab3:
    st.subheader("Regional performance")
    reg = region_performance(f)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            px.bar(reg.sort_values("Revenue"), x="Revenue", y="Region",
                   orientation="h", title="Revenue by region"),
            use_container_width=True
        )
    with c2:
        st.plotly_chart(
            px.bar(reg.sort_values("Profit"), x="Profit", y="Region",
                   orientation="h", title="Profit by region"),
            use_container_width=True
        )

    st.dataframe(
        reg.style.format({
            "Revenue": "₹{:,.0f}", "Profit": "₹{:,.0f}",
            "Profit_Margin": "{:.1%}"
        }),
        use_container_width=True, hide_index=True
    )

with tab4:
    st.subheader("Customer segment analysis")
    seg = segment_performance(f)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            px.bar(seg, x="Customer_Segment", y="Revenue",
                   text_auto=".2s", title="Revenue by segment"),
            use_container_width=True
        )
    with c2:
        st.plotly_chart(
            px.bar(seg, x="Customer_Segment", y="Profit",
                   text_auto=".2s", title="Profit by segment"),
            use_container_width=True
        )

    st.plotly_chart(
        px.scatter(
            seg, x="Customers", y="Revenue", size="Orders",
            color="Profit_Margin", text="Customer_Segment",
            title="Customer base vs. revenue"
        ),
        use_container_width=True
    )

    st.dataframe(
        seg.style.format({
            "Revenue": "₹{:,.0f}", "Profit": "₹{:,.0f}",
            "AOV": "₹{:,.0f}",
            "Revenue_per_Customer": "₹{:,.0f}",
            "Profit_Margin": "{:.1%}"
        }),
        use_container_width=True, hide_index=True
    )

st.divider()
st.caption("Portfolio project: replace the generated CSV in data/ with a real e-commerce transaction dataset when ready.")
