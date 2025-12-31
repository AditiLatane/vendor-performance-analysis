import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename = 'D:\Aditi\Data Analyst Projects\Vender Performance Analysis\logs\ingestion_log.log',
    level = logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

engine = create_engine('sqlite:///inventory.db')

def reduce_memory(df):
    """Downcast numeric columns to save memory"""
    for col in df.columns:
        col_type = df[col].dtype

        if col_type == 'int64':
            df[col] = pd.to_numeric(df[col], downcast='integer')
        elif col_type == 'float64':
            df[col] = pd.to_numeric(df[col], downcast='float')
        elif col_type == 'object':
            # Convert strings to category if few unique values
            if df[col].nunique() / len(df) < 0.5:
                df[col] = df[col].astype('category')
    return df

def ingest_db(df, table_name, engine):
    '''This will ingest df into db tables'''
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

# Loop through CSV files with chunking
def load_raw_data():  
    '''This will load csv as dataframes and ingest into db.'''
    start = time.time()
    for file in os.listdir('D:\Aditi\Data Analyst Projects\Vender Performance Analysis\Datasets\data'):
        if file.endswith('.csv'):
            chunks = []
            for chunk in pd.read_csv(os.path.join('D:\Aditi\Data Analyst Projects\Vender Performance Analysis\Datasets\data', file), chunksize=80000, engine='python'):
                chunk = reduce_memory(chunk)   # optimize each chunk
                chunks.append(chunk)

            df = pd.concat(chunks, ignore_index=True)
            logging.info(f"Ingesting {file} => {df.shape} , memory usage: {df.memory_usage(deep=True).sum()/1024**2:.2f} MB")
            # make chunks to avoid MemoryError 
            # use 'engine=python' to avoid ParseError

            ingest_db(df, file[:-4], engine)
    end = time.time()
    total_time = (end-start)/60
    logging.info('-'*50,'Ingestion Completed','-'*50)
    logging.info(f'\nTotal time taken : {total_time} minutes ')
    
    
if __name__ == '__main__':
    load_raw_data()
