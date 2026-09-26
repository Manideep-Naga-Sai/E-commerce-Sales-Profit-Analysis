import random
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

OUT = Path(__file__).resolve().parents[1] / "data" / "ecommerce_sales.csv"

categories = {
    "Electronics": ["Phones", "Laptops", "Accessories"],
    "Furniture": ["Chairs", "Desks", "Storage"],
    "Office Supplies": ["Paper", "Binders", "Stationery"],
    "Home & Kitchen": ["Kitchen", "Decor", "Appliances"],
    "Sports": ["Fitness", "Outdoor", "Team Sports"],
}

product_templates = [
    ("Smartphone Pro", "Electronics", "Phones", 650, 0.22),
    ("Budget Smartphone", "Electronics", "Phones", 280, 0.18),
    ("Business Laptop", "Electronics", "Laptops", 1100, 0.20),
    ("Wireless Headset", "Electronics", "Accessories", 120, 0.28),
    ("Office Chair", "Furniture", "Chairs", 240, 0.24),
    ("Ergonomic Chair", "Furniture", "Chairs", 420, 0.27),
    ("Standing Desk", "Furniture", "Desks", 520, 0.25),
    ("Filing Cabinet", "Furniture", "Storage", 180, 0.22),
    ("Copy Paper Box", "Office Supplies", "Paper", 45, 0.16),
    ("Premium Binder", "Office Supplies", "Binders", 18, 0.25),
    ("Notebook Pack", "Office Supplies", "Stationery", 24, 0.30),
    ("Coffee Maker", "Home & Kitchen", "Appliances", 160, 0.21),
    ("Cookware Set", "Home & Kitchen", "Kitchen", 210, 0.23),
    ("Wall Decor Set", "Home & Kitchen", "Decor", 75, 0.31),
    ("Treadmill", "Sports", "Fitness", 850, 0.19),
    ("Yoga Mat", "Sports", "Fitness", 35, 0.32),
    ("Camping Tent", "Sports", "Outdoor", 190, 0.26),
    ("Team Jersey", "Sports", "Team Sports", 90, 0.29),
]

regions = {
    "North": ["Delhi", "Chandigarh", "Jaipur"],
    "South": ["Hyderabad", "Bengaluru", "Chennai"],
    "West": ["Mumbai", "Pune", "Ahmedabad"],
    "East": ["Kolkata", "Bhubaneswar", "Guwahati"],
}

segments = ["Consumer", "Corporate", "Small Business"]
segment_weights = [0.58, 0.24, 0.18]

customers = [f"CUST-{i:05d}" for i in range(1, 2501)]
customer_segment = {
    c: random.choices(segments, weights=segment_weights, k=1)[0] for c in customers
}

start = datetime(2024, 1, 1)
days = 730
rows = []

for order_num in range(1, 18001):
    order_id = f"ORD-{order_num:06d}"
    customer = random.choice(customers)
    date = start + timedelta(days=random.randrange(days))
    product_id, product_name, category, subcat, base_price, margin = (
        None, None, None, None, None, None
    )
    p = random.choice(product_templates)
    product_name, category, subcat, base_price, margin = p
    product_id = "PROD-" + str(product_templates.index(p) + 1).zfill(3)

    quantity = random.choices([1, 2, 3, 4, 5], weights=[0.52, 0.28, 0.12, 0.06, 0.02])[0]
    discount = float(np.clip(np.random.beta(2, 8) * 0.55, 0, 0.45))
    # Corporate orders are somewhat larger.
    if customer_segment[customer] == "Corporate":
        quantity += random.choice([0, 1, 2])
        discount = min(0.50, discount + random.uniform(0, 0.08))

    unit_price = round(base_price * np.random.uniform(0.92, 1.08), 2)
    sales = round(quantity * unit_price * (1 - discount), 2)

    # Costs vary with category and discount; some heavily discounted items become low-profit.
    effective_margin = margin - discount * random.uniform(0.55, 1.15)
    cost = round(max(0.15, quantity * unit_price * (1 - effective_margin)), 2)
    profit = round(sales - cost, 2)

    region = random.choice(list(regions.keys()))
    city = random.choice(regions[region])

    rows.append([
        order_id, date.date(), customer, product_id, product_name, category, subcat,
        quantity, unit_price, round(discount, 4), sales, cost, profit,
        region, random.choice(["State A", "State B", "State C"]), city,
        customer_segment[customer]
    ])

cols = [
    "Order_ID","Order_Date","Customer_ID","Product_ID","Product_Name","Category",
    "Sub_Category","Quantity","Unit_Price","Discount","Sales","Cost","Profit",
    "Region","State","City","Customer_Segment"
]

df = pd.DataFrame(rows, columns=cols)
df.to_csv(OUT, index=False)
print(f"Generated {len(df):,} transactions: {OUT}")
