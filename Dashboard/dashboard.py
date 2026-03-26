import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import  pathlib

load_dotenv()

host = st.secrets.get("DB_HOST")
user = st.secrets.get("DB_USER")
password = st.secrets.get("DB_PASSWORD")
database = st.secrets.get("DB_NAME")

st.title("E-Commerce Data Science Dashboard")

repo_root = pathlib.Path(__file__).parent.parent
csv_path = repo_root / "data" / "data.csv"

df = pd.read_csv(csv_path, encoding="latin1")

@st.cache_data
def load_data():
    query = "SELECT * FROM ecommerce_data"
    return pd.read_sql(query, engine)


# try to use SQLAlchemy if available; otherwise fall back to mysql.connector
use_engine = False
try:
    from sqlalchemy import create_engine
    use_engine = True
except ModuleNotFoundError:
    st.warning("SQLAlchemy not installed – using raw mysql.connector connection. "
               "Install it with `pip install sqlalchemy` to remove this message.")

query = "SELECT * FROM ecommerce_data"

if use_engine:
    # password contains '@', so quote it for the URL
    from urllib.parse import quote_plus
    pwd = quote_plus(str(password))
    url = f"mysql+mysqlconnector://{user}:{pwd}@{host} : 3306/{database}"
    engine = create_engine(url)
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Failed to load data via SQLAlchemy: {e}")
        st.stop()
else:
    import mysql.connector
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    try:
        df = pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Failed to load data via mysql.connector: {e}")
        st.stop()

if df.empty:
    st.warning("No data available in ecommerce_data table")
    st.stop()

df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"], format='mixed', errors='coerce')

df["Month"] = df["InvoiceDate"].dt.to_period("M")

st.sidebar.header("Filters")


country = st.sidebar.selectbox(
    "Monthly Sales",
    df["Country"].unique()
)

filtered_df = df[df["Country"] == country]

if filtered_df.empty:
    st.warning("No data available for selected country")
    st.stop()

st.subheader("Dataset Overview")

st.write("Total Rows:", df.shape[0])
st.write("Total Columns:", df.shape[1])
st.write(filtered_df["Country"].value_counts())

st.dataframe(df.head())


st.subheader("Top Selling Products")

top_products = (
    df.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_products)

st.subheader("Revenue by Country")

country_sales = (
    df.groupby("Country")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(country_sales)


monthly_sales = filtered_df.groupby("Month")["TotalPrice"].sum()

st.subheader(f"Monthly Sales Trend")
st.caption(f"{country}")
st.line_chart(monthly_sales)


st.subheader("Top Customers")

top_customers = (
    df.groupby("CustomerID")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_customers)


st.subheader("Business Metrics")

total_revenue = filtered_df["TotalPrice"].sum()
total_orders = filtered_df["InvoiceNo"].nunique()
total_customers = filtered_df["CustomerID"].nunique()

st.write("Total Revenue:", round(total_revenue, 2))
st.write("Total Orders:", total_orders)
st.write("Total Customers:", total_customers)

