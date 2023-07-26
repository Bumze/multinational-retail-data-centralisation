import pandas as pd
import tabula
from sqlalchemy import inspect
import requests
import boto3 

class DataExtractor:

    def __init__(self):
            pass
  
 # Read from RDS database through the engine
    def read_rds_table(self,engine, table_name= 'table_name'):
        with engine.begin() as conn: #engine.begin vs engine.connect. Start connection to engine to allow access to data
            return pd.read_sql_table('table_name', con=conn)# extracting table tagged table_name as a DataFrame   
  
 # Inspect the database for table names
    def list_db_tables(self, engine): 
        inspector = inspect(engine)
        return inspector.get_table_names()
    
 # Retrieve pdf data from given aws link
    def retrieve_pdf_data(self, link):
        link = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
        card_df = pd.concat(tabula.read_pdf(link, pages='all')) # enables table extraction from a PDF and extracts all
        return card_df
    
 # Create dictionary for 2 API endpoints and create method to return number of stores
    API_header = {"x-api-key":"yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"}
    num_of_stores_endpoint ='https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
    retrieve_store_endpoint ='https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}'
 
 # Method to list number of stores to retrieve data from 
    def list_number_of_stores(self, API_header, num_of_stores_endpoint):
        num_of_stores = requests.get(num_of_stores_endpoint, headers=API_header).json()
        return num_of_stores
    
 # This method retrieves data of a number of stores from the given aws link
    def retrieve_store_data(self, retrieve_store_endpoint, num_of_stores_endpoint, API_header):
        num_of_stores = self.list_number_of_stores(API_header, num_of_stores_endpoint)
        stores = []
        for store in range(num_of_stores['number_stores']):# for items in values of the dict key number_stores
            response = requests.get(f'{retrieve_store_endpoint}/{store}', headers=API_header).json()
            stores.append(response)
        stores_df = pd.DataFrame(stores)
        return stores_df
    
 # This method extracts products_data from AWS S3 
    address = "s3://data-handling-public/products.csv"
    def extract_from_s3(self, address):
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket='data-handling-public', Key='products.csv')
        products_df = pd.read_csv(obj['Body'])
        return products_df

if __name__ == '__main__':

    dataExtractor = DataExtractor()    

