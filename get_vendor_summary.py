import pandas as pd
import sqlite3
import logging
from ingestion_db import ingest_db
import time

logging.basicConfig(
    filename='logs/get_vendor_summary.log',
    level=logging.DEBUG,
    format='%(asctime) - %(levelname)s - %(message)s',
    filemode = "a" 
)

def create_vendor_summary(conn):
    '''This function will merge different tables to get the overall vendor summary and adding new columns in resultant data.'''
    vendor_sales_summary = pd.read_sql_query("""
    with FreightSummary as (
        select VendorNumber, sum(Freight) as FreightCost 
        from vendor_invoice 
        group by VendorNumber
    ),
    PurchasesSummary as(
        select p.VendorNumber, p.VendorName, p.Brand, p.PurchasePrice, p.Description, 
        pp.Price as ActualPrice, pp.Volume,
        sum(p.Quantity) as TotalPurchaseQuantity,
        sum(p.Dollars) as TotalPurchaseDollars
        from purchases p
        join purchase_prices pp
        on p.Brand=pp.Brand
        where p.PurchasePrice>0
        group by p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
    ),  
    SalesSummary as (
        select VendorNo, Brand,
        sum(SalesDollars) as TotalSalesDollars,
        sum(SalesPrice) as TotalSalesPrice,
        sum(SalesQuantity) as TotalSalesQuantity,
        sum(ExciseTax) as TotalExciseTax
        from sales
        group by VendorNo, Brand
    )


    select
    ps.VendorNumber, 
    ps.VendorName,                      
    ps.Brand,
    ps.Description,
    ps.PurchasePrice, 
    ps.ActualPrice,
    ps.Volume,
    ps.TotalPurchaseQuantity,
    ps.TotalPurchaseDollars,
    ss.TotalSalesQuantity,
    ss.TotalSalesDollars,
    ss.TotalSalesPrice,
    ss.TotalExciseTax,
    fs.FreightCost

    from PurchasesSummary ps
    left join SalesSummary ss on ps.VendorNumber=ss.VendorNo and ps.Brand=ss.Brand 
    left join FreightSummary fs on ps.VendorNumber=fs.VendorNumber

    order by ps.TotalPurchaseDollars desc""", conn)

    return vendor_sales_summary

def clean_data(df):
    '''This function will clean the data'''
    # change datatype from object to float
    df['Volume'] = df['Volume'].astype('float')
    # fill missing values with 0
    df.fillna(0, inplace=True)
    # remove extra spaces from categorical columns
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()
    # Creating new columns for better analysis
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = ( df['GrossProfit'] / df['TotalSalesDollars']) * 100
    df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']
    df['SalesToPurchaseRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars']
    
    return df

if __name__ == '__main__' :
    # creating db connection 
    conn = sqlite3.connect('inventory.db')

    start = time.time()
    logging.info('Creating Vendor Summary Table......')
    summary_df = create_vendor_summary(conn) 
    end = time.time()

    logging.info(f'Created Vendor Summary Table in {(end-start)/60:.2f} minutes.')
    logging.info(summary_df.head())

    start = time.time()
    logging.info('Cleaning Data......')
    clean_df = clean_data(summary_df) 
    end = time.time()
    
    logging.info(f'Cleaned data in {(end-start)/60:.2f} minutes.')
    logging.info(clean_df.head())

    start = time.time()
    logging.info('Ingesting Data......')
    ingest_db(clean_df, 'vendor_sales_summary', conn)
    end = time.time()

    logging.info(f'Ingested data in {(end-start)/60:.2f} minutes.')
    logging.info('Data Ingestion is Completed !')
    