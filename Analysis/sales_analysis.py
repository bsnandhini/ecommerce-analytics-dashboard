import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Connect to database
conn = sqlite3.connect("Database/ecommerce.db")

query = """
SELECT o.order_date, oi.total_price
FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id;
"""

df = pd.read_sql(query, conn)

# Convert to datetime
df["order_date"] = pd.to_datetime(df["order_date"])

# Extract month
df["month"] = df["order_date"].dt.to_period("M")

# Group by month
monthly_sales = df.groupby("month")["total_price"].sum()

# Convert index to string
monthly_sales.index = monthly_sales.index.astype(str)

# Plot chart
# Plot Smooth Line with Markers
plt.figure()
plt.figure()
plt.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker='o',
    color='royalblue',
    markerfacecolor='white',
    markeredgecolor='royalblue',
    linewidth=2
)

plt.xticks(rotation=45)
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Total Revenue")

plt.tight_layout()
plt.show()

conn.close()











