import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 E-commerce Analytics Dashboard")

#CUSTOM KPI CARD DESIGN

st.markdown("""
<style>

.kpi-card{
background-color:#ffffff;
padding:20px;
border-radius:12px;
box-shadow:0 4px 12px rgba(0,0,0,0.1);
text-align:center;
}

.kpi-title{
font-size:16px;
color:#666;
}

.kpi-value{
font-size:32px;
font-weight:bold;
margin-top:5px;
}

.green{border-left:6px solid #00C853;}
.blue{border-left:6px solid #2979FF;}
.orange{border-left:6px solid #FF9100;}
.purple{border-left:6px solid #AA00FF;}

</style>
""", unsafe_allow_html=True)

# DATABASE CONNECTION

conn = sqlite3.connect("Database/ecommerce.db")

## LOAD DATA
query = """
SELECT
o.order_id,
o.order_date,
c.customer_id,
c.country,
oi.product_id,
oi.quantity,
oi.total_price
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
JOIN order_items oi
ON o.order_id = oi.order_id
"""

df = pd.read_sql(query, conn)

df["order_date"] = pd.to_datetime(df["order_date"])

# SIDEBAR FILTERS

st.sidebar.header("🔎 Filters")

start_date = st.sidebar.date_input(
"Start Date",
df["order_date"].min()
)

end_date = st.sidebar.date_input(
"End Date",
df["order_date"].max()
)

products = df["product_id"].unique()

selected_products = st.sidebar.multiselect(
"Select Products",
products,
default=products
)

countries = df["country"].unique()

selected_countries = st.sidebar.multiselect(
"Select Countries",
countries,
default=countries
)

# APPLY FILTERS
filtered_df = df[
(df["product_id"].isin(selected_products)) &
(df["country"].isin(selected_countries)) &
(df["order_date"] >= pd.to_datetime(start_date)) &
(df["order_date"] <= pd.to_datetime(end_date))
]

# KPI CALCULATIONS

revenue = filtered_df["total_price"].sum()
orders = filtered_df["order_id"].nunique()
customers = filtered_df["customer_id"].nunique()
products_count = filtered_df["product_id"].nunique()

# KPI CARDS

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card green">
        <div class="kpi-title">💰 Total Revenue</div>
        <div class="kpi-value">${revenue:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card blue">
        <div class="kpi-title">📦 Orders</div>
        <div class="kpi-value">{orders}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card orange">
        <div class="kpi-title">👤 Customers</div>
        <div class="kpi-value">{customers}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card purple">
        <div class="kpi-title">🛒 Products</div>
        <div class="kpi-value">{products_count}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# MONTHLY REVENUE

filtered_df["month"] = filtered_df["order_date"].dt.to_period("M").astype(str)

monthly = filtered_df.groupby("month")["total_price"].sum().reset_index()

fig1 = px.line(
monthly,
x="month",
y="total_price",
markers=True,
title="📈 Monthly Revenue Trend",
animation_frame="month"
)

st.plotly_chart(fig1,use_container_width=True)

# TWO COLUMN CHART LAYOUT

col1,col2 = st.columns(2)

# TOP PRODUCTS

top_products = (
filtered_df.groupby("product_id")["quantity"]
.sum()
.reset_index()
.sort_values(by="quantity",ascending=False)
.head(10)
)

fig2 = px.bar(
top_products,
x="product_id",
y="quantity",
color="quantity",
title="🔥 Top 10 Selling Products"
)

col1.plotly_chart(fig2,use_container_width=True)

# COUNTRY MAP

country_sales = (
filtered_df.groupby("country")["total_price"]
.sum()
.reset_index()
)

fig3 = px.choropleth(
country_sales,
locations="country",
locationmode="country names",
color="total_price",
color_continuous_scale="Blues",
title="🌍 Revenue by Country"
)

col2.plotly_chart(fig3,use_container_width=True)


# TOP CUSTOMERS

top_customers = (
filtered_df.groupby("customer_id")["order_id"]
.count()
.reset_index()
.sort_values(by="order_id",ascending=False)
.head(10)
)

fig4 = px.bar(
top_customers,
x="customer_id",
y="order_id",
color="order_id",
title="🏆 Top Customers by Orders"
)

st.plotly_chart(fig4,use_container_width=True)

# DATA TABLE

st.markdown("### 📄 Filtered Data")
st.dataframe(filtered_df)

# FOOTER

st.markdown("---")
st.caption("Professional E-commerce Dashboard | Streamlit + Plotly + SQLite")

