import streamlit as st
import pandas as pd

st.title("E-Commerce Data Science Dashboard")

# Load database config from Streamlit secrets
config = st.secrets["mysql"]
host = config["host"]
user = config["user"]
password = config["password"]
database = config["database"]
port = config["port"]

query = "SELECT * FROM ecommerce_data"

# Try using SQLAlchemy
@st.cache_data
def load_data_sqlalchemy():
    from sqlalchemy import create_engine
    from urllib.parse import quote_plus

    pwd = quote_plus(password)
    url = f"mysql+mysqlconnector://{user}:{pwd}@{host}:{port}/{database}"

    engine = create_engine(url, connect_args={"ssl_disabled": False})
    return pd.read_sql(query, engine)

# Fallback to mysql.connector
@st.cache_data
def load_data_connector():
    import mysql.connector
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
        ssl_disabled=False
    )
    return pd.read_sql(query, conn)


# Try SQLAlchemy → fallback to mysql.connector
try:
    df = load_data_sqlalchemy()
except Exception as e:
    st.warning(f"SQLAlchemy error, trying mysql.connector: {e}")
    try:
        df = load_data_connector()
    except Exception as e2:
        st.error(f"Could not load data from MySQL: {e2}")
        st.stop()


# No data?
if df.empty:
    st.warning("No data in ecommerce_data table.")
    st.stop()

# Data cleaning
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
df["Month"] = df["InvoiceDate"].dt.to_period("M")

# Sidebar
st.sidebar.header("Filters")
country = st.sidebar.selectbox("Select Country", df["Country"].unique())

filtered_df = df[df["Country"] == country]
if filtered_df.empty:
    st.warning("No data for this country.")
    st.stop()

# Overview
st.subheader("Dataset Overview")
st.write(f"Total Rows: {df.shape[0]}")
st.write(f"Total Columns: {df.shape[1]}")
st.write(filtered_df["Country"].value_counts())
st.dataframe(df.head())

# Top Products
st.subheader("Top Selling Products")
top_products = (
    df.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
st.bar_chart(top_products)

# Revenue by Country
st.subheader("Revenue by Country")
country_sales = (
    df.groupby("Country")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
st.bar_chart(country_sales)

# Monthly Trend
monthly_sales = filtered_df.groupby("Month")["TotalPrice"].sum()
st.subheader(f"Monthly Sales Trend — {country}")
st.line_chart(monthly_sales)

# Top Customers
st.subheader("Top Customers")
top_customers = (
    df.groupby("CustomerID")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
st.bar_chart(top_customers)

# Business Metrics
st.subheader("Business Metrics")
total_revenue = filtered_df["TotalPrice"].sum()
total_orders = filtered_df["InvoiceNo"].nunique()
total_customers = filtered_df["CustomerID"].nunique()

st.write("Total Revenue:", round(total_revenue, 2))
st.write("Total Orders:", total_orders)
st.write("Total Customers:", total_customers)
