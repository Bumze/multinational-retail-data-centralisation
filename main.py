import pandas as pd
from sqlalchemy import inspect, create_engine
from database_utils import DatabaseConnector
from data_cleaning import DataCleaning
from data_extraction import DataExtractor


if __name__ == '__main__':
    databaseConnector = DatabaseConnector()
    dataExtractor = DataExtractor()    
    dataCleaning = DataCleaning()

 # extract and clean the users and order tables -->connect to source through engine/credentials
    link = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
    creds1 = databaseConnector.read_db_creds('db_creds.yaml')
    engine = databaseConnector.init_db_engine(creds1)
    
    # check tables
    table_list = dataExtractor.list_db_tables(engine)

    # extract and clean user details
    user_df = dataExtractor.read_rds_table(engine, table_name='legacy_users')
    clean_user_data = dataCleaning.clean_user_data(user_df) 

 # extract cleaned card details
    card_df = dataExtractor.retrieve_pdf_data(link)
    clean_card_data = dataCleaning.clean_card_data(card_df)

 # stores and orders extraction details 
    API_header ={"x-api-key":"yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"}
    num_of_stores_endpoint ='https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
    retrieve_store_endpoint ='https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details'

    # To call stores data cleaning  
    num_of_stores = dataExtractor.list_number_of_stores(API_header, num_of_stores_endpoint)
    stores_df = dataExtractor.retrieve_store_data(retrieve_store_endpoint, num_of_stores_endpoint, API_header)
    clean_stores_data = dataCleaning.clean_store_data(stores_df)

    # To call orders data cleaning
    orders_df = dataExtractor.read_rds_table(engine, table_name='orders_table')
    clean_orders_data = dataCleaning.clean_orders_data(orders_df) 

 # extract cleaned products details
    address = "s3://data-handling-public/products.csv"
    products_df = dataExtractor.extract_from_s3(address)
    clean_products_data = dataCleaning.clean_products_data(products_df) 

 # extract cleaned date times 
    link = 'http://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'
    dates_df = dataExtractor.extract_json(link)
    clean_dates_data = dataCleaning.clean_dates_data(dates_df) 

 # upload various cleaned data to local postgresql server  
    #set up
    creds = databaseConnector.read_db_creds('local_db_creds.yaml')
    my_engine = databaseConnector.init_db_engine(creds)
    #upload
    upload_user_data = databaseConnector.upload_to_db(clean_user_data,'dim_users', my_engine)
    upload_orders_table = databaseConnector.upload_to_db(clean_orders_data, 'orders_table', my_engine)
    upload_products_data = databaseConnector.upload_to_db(clean_products_data,'dim_products', my_engine)
    gitupload_date_data = databaseConnector.upload_to_db(clean_dates_data,'dim_date_times', my_engine)
   
   #  clean_orders_data.info()
   