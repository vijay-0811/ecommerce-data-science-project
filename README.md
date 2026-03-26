# E-Commerce Data Science Project

## Project Overview

This project analyzes a large e-commerce transaction dataset and builds an end-to-end data science pipeline including data storage, analysis, machine learning, and an interactive dashboard.

The goal of the project is to extract business insights from transaction data and segment customers based on their purchasing behavior.

## Dataset

The dataset contains more than **540,000 e-commerce transactions** including information such as:

* Invoice number
* Product description
* Quantity purchased
* Price per item
* Customer ID
* Country
* Transaction date

## Technologies Used

* Python
* SQL
* MySQL
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Streamlit

## Project Pipeline

Data Collection
↓
Data Cleaning and Processing using Pandas
↓
Database Storage using MySQL
↓
SQL Business Analysis
↓
Customer Segmentation using Machine Learning
↓
Interactive Dashboard using Streamlit

## SQL Analysis

The project also includes business analytics queries written in SQL.

Examples include:
- Total revenue calculation
- Top selling products
- Revenue by country
- Monthly sales trends
- Top customers

All queries are available in:
sql/analysis_queries.sql

## Key Features

### Sales Analysis

* Identify top-selling products
* Revenue trends over time
* Sales distribution by country

### Customer Segmentation

Customers are grouped using **K-Means Clustering** to identify different types of buyers based on purchase behavior.

### Interactive Dashboard

The Streamlit dashboard provides:

* Revenue analytics
* Country-level insights
* Top customers
* Top products
* Monthly sales trends

## Dashboard

Run the dashboard using:

streamlit run dashboard/dashboard.py

## Project Structure

ecommerce-data-science-project

data
  data.csv
  customer_segments.csv

scripts
  main.py
  upload_to_mysql.py
  customer_segmentation.py

dashboard
  dashboard.py

requirements.txt
README.md

## Future Improvements

* Deploy the dashboard online
* Add more advanced machine learning models
* Add interactive filters and KPIs
* Improve visualizations

## Author

Vijay Prajapati
Ahmedabad, Gujarat

LinkedIn: https://www.linkedin.com/in/vijayprajapati0811/
GitHub: https://github.com/vijay-0811


