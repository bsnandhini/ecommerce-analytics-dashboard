import sqlite3
import pandas as pd

conn = sqlite3.connect("database/ecommerce.db")

query = """
SELECT customer_id, SUM(total_price) as total_spent
FROM orders
JOIN order_items USING(order_id)
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10
"""

df = pd.read_sql(query, conn)
print(df)

import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(8,5))

colors = plt.cm.viridis(np.linspace(0,1,len(df)))

plt.bar(df["customer_id"].astype(str), df["total_spent"], color=colors)

plt.title("Top 10 Customers by Total Spending")
plt.xlabel("Customer ID")
plt.ylabel("Total Spent")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()