import pandas as pd
from sqlalchemy import inspect, create_engine
from database_utils import DatabaseConnector
from data_cleaning import DataCleaning
from data_extraction import DataExtractor
import psycopg2


if __name__ == '__main__':
    databaseConnector = DatabaseConnector()
    dataExtractor = DataExtractor()    
    dataCleaning = DataCleaning()

 # extraction and cleaning the users and order tables
    link = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
    creds1 = databaseConnector.read_db_creds('db_creds.yaml')
    engine = databaseConnector.init_db_engine(creds1)
    print(engine)
    
    # check tables
    table_list = dataExtractor.list_db_tables(engine)

 # extract cleaned user details
    user_df = dataExtractor.read_rds_table(engine, table_name='legacy_users')
    clean_user_data = dataCleaning.clean_users_data(user_df) 

    card_df = dataExtractor.retrieve_pdf_data(link)
    clean_card_data = dataCleaning.clean_card_data(card_df)


 # store extraction details 
    API_header ={"x-api-key":"yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"}
    num_of_stores_endpoint ='https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
    retrieve_store_endpoint ='https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details'
    # To call stores cleaning  
    num_of_stores = dataExtractor.list_number_of_stores(API_header, num_of_stores_endpoint)
    stores_df = dataExtractor.retrieve_store_data(retrieve_store_endpoint, num_of_stores_endpoint, API_header)
    clean_stores_data = dataCleaning.clean_store_data(stores_df)

 # products extraction and cleaning
    address = "s3://data-handling-public/products.csv"
    products_df = dataExtractor.extract_from_s3(address)
    clean_products_data = dataCleaning.clean_products_data(products_df)

 # extract cleaned order details
    orders_df = dataExtractor.read_rds_table(engine, table_name='orders_table')
    clean_orders_data = dataCleaning.clean_orders_data(orders_df) 

 # upload cleaned various data to local postgresql server 
    creds = databaseConnector.read_db_creds('local_db_creds.yaml')
    my_engine = databaseConnector.init_db_engine(creds)
    
   #  my_engine = create_engine(f"{'postgresql'}+{'psycopg2'}://{creds['LOCAL_USER']}:{creds['PASSWORD']}@{creds['LOCAL_HOST']}:{creds['LOCAL_PORT']}/{creds['LOCAL_DATABASE']}")
   #  upload_user_data = databaseConnector.upload_to_db(clean_user_data,'dim_users', my_engine)
   #  upload_orders_table = databaseConnector.upload_to_db(clean_orders_data, 'orders_table', my_engine)
   #  upload_products_data = databaseConnector.upload_to_db(clean_products_data,'dim_products', my_engine)
   #  upload_stores_data = databaseConnector.upload_to_db(clean_stores_data,'dim_store_details', my_engine)
   #  upload_card_data = databaseConnector.upload_to_db(clean_card_data,'dim_card_details', my_engine)
   
    print(table_list)
   