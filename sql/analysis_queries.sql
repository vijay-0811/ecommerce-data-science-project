-- Total Revenue 
SELECT 
SUM(Quantity * UnitPrice) AS total_revenue
FROM ecommerce_data;

-- Top 10 Products
SELECT 
Description,
SUM(Quantity) AS total_sold
FROM ecommerce_data
GROUP BY Description
ORDER BY total_sold DESC
LIMIT 10;

-- Revenue by Country
SELECT 
Country,
SUM(Quantity * UnitPrice) AS revenue
FROM ecommerce_data
GROUP BY Country
ORDER BY revenue DESC;

-- Top 10 Customers 
SELECT 
CustomerID,
SUM(Quantity * UnitPrice) AS total_spent
FROM ecommerce_data
GROUP BY CustomerID
ORDER BY total_spent DESC
LIMIT 10;

-- Monthly Sales
SELECT 
DATE_FORMAT(InvoiceDate, '%Y-%m') AS month,
SUM(Quantity * UnitPrice) AS revenue
FROM ecommerce_data
GROUP BY month
ORDER BY month;