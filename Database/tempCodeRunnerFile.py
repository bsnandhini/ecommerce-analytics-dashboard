import pandas as pd
import sqlite3

#1.Load dataset
df = pd.read_csv("data/online_retail.csv", encoding="ISO-8859-1")

#2. Clean data
df = df.dropna(subset=["CustomerID"])
df = df[df["Quantity"] > 0]
df = df[df["UnitPrice"] > 0]

df["CustomerID"] = df["CustomerID"].astype(int)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], dayfirst=True)

#3.Create Total Price column
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

#4. Connect to SQLite
conn = sqlite3.connect("Database/ecommerce.db")

#5. Create Tables
with open("Database/create_tables.sql", "r") as f:
    conn.executescript(f.read())

#6.Insert Customers
customers = df[["CustomerID", "Country"]].drop_duplicates()
customers.columns = ["customer_id", "country"]
customers.to_sql("customers", conn, if_exists="replace", index=False)

#7.Insert Products
products = df[["StockCode", "Description", "UnitPrice"]].drop_duplicates()
products.columns = ["product_id", "description", "unit_price"]
products.to_sql("products", conn, if_exists="replace", index=False)

#8.Insert Orders
orders = df[["InvoiceNo", "CustomerID", "InvoiceDate"]].drop_duplicates()
orders.columns = ["order_id", "customer_id", "order_date"]
orders.to_sql("orders", conn, if_exists="replace", index=False)

#9.Insert Order Items
order_items = df[["InvoiceNo", "StockCode", "Quantity", "TotalPrice"]]
order_items.columns = ["order_id", "product_id", "quantity", "total_price"]
order_items.to_sql("order_items", conn, if_exists="replace", index=False)

print("✅ Database Created Successfully!")