# Vendor Performance Analysis

## Project Overview

This project focuses on analyzing vendor performance by integrating data from multiple sources, creating a consolidated dataset, performing detailed analysis, answering key business questions, and presenting insights through a report and a Power BI dashboard.

---

## Skills utilized

* Python (Matplotlib, Seaborn, Pandas)
* SQL (Joins)
* Scripting
* Report Writing
* Dashboarding (PowerBI)

---

## Project Steps

### 1. Data Ingestion

* Wrote a Python script to load data from the database in **small chunks**
* Script name: `ingestion_db.py`
* Used **Python** and **logging** for data ingestion

---

### 2. Data Understanding, Joining & Feature Engineering

* Performed **Exploratory Data Analysis (EDA)** to:

  * Find the exact relationship between all tables
  * Identify which records should be analyzed
* Identified relationship:

  ```
  vendor_invoice + purchase_prices = purchases
  ```
* Joined multiple tables using **SQL**:

  * `begin_inventory.csv`
  * `end_inventory.csv`
  * `purchase_prices.csv`
  * `purchases.csv`
  * `sales.csv`
  * `vendor_invoice.csv`
* Script used for joining:

  * `get_vendor_summary.py`
* Converted the joined data into a single table:

  * `vendor_sales_summary`
* Cleaned the data and created new features:

  * `GrossProfit`
  * `ProfitMargin`
  * `StockTurnover`
  * `SalestoPurchaseRatio`

---

### 3. Store Derived Dataset

* Stored the `vendor_sales_summary` back into the database
* Saved it as a **vendor_sales_summary** table using SQL

---

### 4. Data Analysis

* Analyzed the derived dataset (`vendor_sales_summary`) using Python
* Performed:

  * Summary statistics analysis
  * Distribution analysis of numerical columns
  * Filtering to remove inconsistencies
  * Correlation analysis between numerical columns

---

### 5. Business Questions Answered

* **Q1:** Identify brands that need promotion or pricing adjustments which exhibit lower sales performance but higher profit margin
* **Q2:** Which vendors and brands demonstrate the highest sales performance
* **Q3:** Which vendors contribute the most to the total purchase dollars
* **Q4:** How much of total procurement is dependent on the top vendor
* **Q5:** Does purchasing in bulk reduce the unit price, and what is the optimal purchase volume for saving cost
* **Q6:** Which vendors have low inventory turnover, indicating excess stock and slow-moving products
* **Q7:** How much capital is locked in unsold inventory per vendor, and which vendor contributes the most to it
* **Q8:** What is the 95% confidence interval for profit margin of top-performing and low-performing vendors
* **Q9:** Is there a significant difference in profit margin between top-performing and low-performing vendors

---

### 6. Reporting & Recommendations

* Wrote a detailed report
* Provided a few recommendations based on analysis

---

### 7. Visualization

* Created a **Power BI dashboard** to showcase all findings and insights

---

## Project Artifacts

* `ingestion_db.py` – Data ingestion from database
* `get_vendor_summary.py` – SQL-based table joining and summary creation
* `vendor_sales_summary` – Final derived dataset
* Report with recommendations
* Power BI dashboard showcasing results

---

## Conclusion

This project delivers a complete vendor performance analysis workflow, from data ingestion and transformation to business insights and visualization, enabling data-driven decision-making.

---

<img width="1010" height="569" alt="image" src="https://github.com/user-attachments/assets/36d73cc9-ebdf-4022-9015-e4197f969033" />


