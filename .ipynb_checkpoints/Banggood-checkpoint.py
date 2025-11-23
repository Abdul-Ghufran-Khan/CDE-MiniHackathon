import pyodbc
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit page config
st.set_page_config(page_title="Banggood Products Dashboard", layout="wide")

# SQL Server connection
conn = pyodbc.connect(
   "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-G6ELT03;"
    "Database=Banggood;"
    "Trusted_Connection=yes;"
)


# 1. Average price per category
avg_price_query = """
SELECT category, AVG(price) AS AvgPrice
FROM BanggoodProducts
GROUP BY category
ORDER BY AvgPrice DESC;
"""
avg_price = pd.read_sql(avg_price_query, conn)

# 2. Average rating per category
avg_rating_query = """
SELECT category, AVG(rating) AS AvgRating
FROM BanggoodProducts
GROUP BY category
ORDER BY AvgRating DESC;
"""
avg_rating = pd.read_sql(avg_rating_query, conn)

# 3. Product count per category
product_count_query = """
SELECT category, COUNT(*) AS ProductCount
FROM BanggoodProducts
GROUP BY category
ORDER BY ProductCount DESC;
"""
product_count = pd.read_sql(product_count_query, conn)

# 4. Top 5 reviewed items per category
top_reviewed_query = """
WITH RankedProducts AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY review_count DESC) AS rn
    FROM BanggoodProducts
)
SELECT category, title, review_count, price, rating
FROM RankedProducts
WHERE rn <= 5
ORDER BY category, review_count DESC;
"""
top_reviewed = pd.read_sql(top_reviewed_query, conn)

# 5. Stock availability percentage per category
stock_query = """
SELECT category,
       COUNT(*) AS TotalProducts,
       SUM(CASE WHEN availability = 'In Stock' THEN 1 ELSE 0 END) AS InStockCount,
       CAST(SUM(CASE WHEN availability = 'In Stock' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS InStockPercentage
FROM BanggoodProducts
GROUP BY category
ORDER BY InStockPercentage DESC;
"""
stock_availability = pd.read_sql(stock_query, conn)


st.title("Banggood Products Dashboard")

st.header("1️⃣ Average Price per Category")
st.dataframe(avg_price)

st.header("2️⃣ Average Rating per Category")
st.dataframe(avg_rating)

st.header("3️⃣ Product Count per Category")
st.dataframe(product_count)

st.header("4️⃣ Top 5 Reviewed Items per Category")
st.dataframe(top_reviewed)

st.header("5️⃣ Stock Availability Percentage per Category")
st.dataframe(stock_availability)


st.header("📊 Average Price per Category (Bar Chart)")
fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(data=avg_price, x='category', y='AvgPrice', palette='viridis', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

st.header("📊 Average Rating per Category (Bar Chart)")
fig2, ax2 = plt.subplots(figsize=(10,5))
sns.barplot(data=avg_rating, x='category', y='AvgRating', palette='plasma', ax=ax2)
plt.xticks(rotation=45)
st.pyplot(fig2)
