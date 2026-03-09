import sqlite3
import pandas as pd

conn = sqlite3.connect("database/ecommerce.db")

query = """
SELECT product_id, SUM(quantity) as total_sold
FROM order_items
GROUP BY product_id
ORDER BY total_sold DESC
LIMIT 10
"""

df = pd.read_sql(query, conn)
print(df)

import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(8,5))

colors = plt.cm.viridis(np.linspace(0,1,len(df)))

plt.barh(df["product_id"].astype(str), df["total_sold"], color=colors)

plt.title("Top 10 Products by Quantity Sold")
plt.xlabel("Total Quantity Sold")
plt.ylabel("Product ID")

plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()