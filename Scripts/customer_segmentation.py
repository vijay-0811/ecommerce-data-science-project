import pandas as pd
import mysql.connector
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")


# Connect to MySQL
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

query = "SELECT * FROM ecommerce_data"
df = pd.read_sql(query, conn)

# Create TotalPrice column
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

# Customer summary
customer_df = df.groupby("CustomerID").agg({
    "InvoiceNo":"count",
    "TotalPrice":"sum",
    "Quantity":"sum"
})

customer_df.columns = ["TotalOrders","TotalSpent","TotalQuantity"]

print(customer_df.head())



# Machine Learning 
scaler = StandardScaler()
scaled_data = scaler.fit_transform(customer_df)

kmeans = KMeans(n_clusters=3, random_state=42)

customer_df["Cluster"] = kmeans.fit_predict(scaled_data)

print(customer_df.head())


plt.scatter(customer_df["TotalOrders"], customer_df["TotalSpent"], c=customer_df["Cluster"])

plt.xlabel("Total Orders")
plt.ylabel("Total Money Spent")
plt.title("Customer Segmentation")

plt.show()

customer_df.to_csv("customer_"
".csv")
print("Customer segmentation saved!")

df.to_csv("data/customer_segments.csv", index=False)