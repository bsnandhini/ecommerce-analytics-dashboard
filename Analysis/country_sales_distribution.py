import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to database
conn = sqlite3.connect("database/ecommerce.db")

query = """
SELECT c.country, SUM(oi.total_price) as total_sales
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.country
ORDER BY total_sales DESC LIMIT 15
"""

df = pd.read_sql(query, conn)

print(df)

# Plot Pie Chart
plt.figure(figsize=(7,7))

plt.pie(
    df["total_sales"],
    labels=df["country"],
    autopct="%1.1f%%",
    startangle=140
)

plt.title("Country-wise Sales Distribution")

plt.tight_layout()
plt.show()

conn.close()