import pandas as pd 
import matplotlib.pyplot as plt 

df = pd.read_csv("data/data.csv" , encoding="latin1")

print("\n top 5 data ")
print(df.head())

print(df.info())

print("\n missing value")
print(df.isnull().sum())


df = df.dropna(subset=["CustomerID"])

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

print("\n Clean DataSet")
print(df.head())

top_productes = df.groupby("Description")["Quantity"].sum().sort_values(ascending=False).head(10)

print("\n Top Selling Products")
print(top_productes)

top_productes.plot(kind="bar")

plt.title("Top Selling Products")
plt.xlabel("Product")
plt.ylabel("Quantity Sold")

plt.show()


df["Month"] = df["InvoiceDate"].dt.to_period("M")

monthly_sales = df.groupby("Month")["TotalPrice"].sum()

print("\nMonthly Revenue")
print(monthly_sales)

monthly_sales.plot()

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.show()

