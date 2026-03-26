import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

# Load CSV
df = pd.read_csv("data/data.csv", encoding="latin1")
# parse InvoiceDate to datetime, invalid parsing will become NaT
if 'InvoiceDate' in df.columns:
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')

# Connect to MySQL
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cursor = conn.cursor()

# Insert data
for i, row in df.iterrows():
    sql = """
    INSERT INTO ecommerce_data
    (InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """
    # convert pandas NaN to None so MySQL receives NULL instead of unquoted nan
    values = (
        None if pd.isna(row['InvoiceNo']) else row['InvoiceNo'],
        None if pd.isna(row['StockCode']) else row['StockCode'],
        None if pd.isna(row['Description']) else row['Description'],
        None if pd.isna(row['Quantity']) else row['Quantity'],
        None if pd.isna(row['InvoiceDate']) else row['InvoiceDate'],
        None if pd.isna(row['UnitPrice']) else row['UnitPrice'],
        None if pd.isna(row['CustomerID']) else row['CustomerID'],
        None if pd.isna(row['Country']) else row['Country'],
    )

    try:
        cursor.execute(sql, values)
    except mysql.connector.Error as e:
        print(f"Failed to insert row {i}: {e}")
        # depending on requirements, either continue or break
        continue

conn.commit()

print("Data inserted successfully!")

cursor.close()
conn.close()
