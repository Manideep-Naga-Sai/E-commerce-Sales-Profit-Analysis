-- DuckDB / PostgreSQL-style business analysis.
-- Table name assumed: sales

-- 1. Executive KPIs
SELECT
    SUM(Sales) AS Revenue,
    SUM(Profit) AS Profit,
    COUNT(DISTINCT Order_ID) AS Orders,
    COUNT(DISTINCT Customer_ID) AS Customers,
    SUM(Sales) / COUNT(DISTINCT Order_ID) AS AOV,
    SUM(Profit) / NULLIF(SUM(Sales), 0) AS Profit_Margin
FROM sales;

-- 2. Monthly performance and growth
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', Order_Date) AS Month,
        SUM(Sales) AS Revenue,
        SUM(Profit) AS Profit,
        COUNT(DISTINCT Order_ID) AS Orders
    FROM sales
    GROUP BY 1
)
SELECT
    Month,
    Revenue,
    Profit,
    Orders,
    Revenue / NULLIF(Orders, 0) AS AOV,
    (Revenue / LAG(Revenue) OVER (ORDER BY Month)) - 1 AS Revenue_MoM_Growth,
    (Profit / LAG(Profit) OVER (ORDER BY Month)) - 1 AS Profit_MoM_Growth
FROM monthly
ORDER BY Month;

-- 3. Top 10 products by revenue
SELECT
    Product_ID,
    Product_Name,
    SUM(Sales) AS Revenue,
    SUM(Profit) AS Profit,
    SUM(Quantity) AS Units,
    SUM(Profit) / NULLIF(SUM(Sales), 0) AS Profit_Margin
FROM sales
GROUP BY 1, 2
ORDER BY Revenue DESC
LIMIT 10;

-- 4. Categories
SELECT
    Category,
    SUM(Sales) AS Revenue,
    SUM(Profit) AS Profit,
    COUNT(DISTINCT Order_ID) AS Orders,
    SUM(Profit) / NULLIF(SUM(Sales), 0) AS Profit_Margin
FROM sales
GROUP BY Category
ORDER BY Revenue DESC;

-- 5. Regions
SELECT
    Region,
    SUM(Sales) AS Revenue,
    SUM(Profit) AS Profit,
    COUNT(DISTINCT Order_ID) AS Orders,
    SUM(Profit) / NULLIF(SUM(Sales), 0) AS Profit_Margin
FROM sales
GROUP BY Region
ORDER BY Profit DESC;

-- 6. Customer segments
SELECT
    Customer_Segment,
    COUNT(DISTINCT Customer_ID) AS Customers,
    COUNT(DISTINCT Order_ID) AS Orders,
    SUM(Sales) AS Revenue,
    SUM(Profit) AS Profit,
    SUM(Sales) / COUNT(DISTINCT Order_ID) AS AOV,
    SUM(Profit) / NULLIF(SUM(Sales), 0) AS Profit_Margin
FROM sales
GROUP BY Customer_Segment
ORDER BY Revenue DESC;

-- 7. Discount vs profitability
SELECT
    CASE
        WHEN Discount < 0.10 THEN '0-10%'
        WHEN Discount < 0.20 THEN '10-20%'
        WHEN Discount < 0.30 THEN '20-30%'
        ELSE '30%+'
    END AS Discount_Band,
    SUM(Sales) AS Revenue,
    SUM(Profit) AS Profit,
    SUM(Profit) / NULLIF(SUM(Sales), 0) AS Profit_Margin
FROM sales
GROUP BY 1
ORDER BY 1;
