
## Introduction


This Project is completed as the fourth in a required list of projects at Aicore. Systems with fully centralised database are required by a Multinational Store to enable them become more data-driven, and make sales data accessible from one centralised location. The system is designed, data in different formats is extracted from various sources. It is rigorously transformed then loaded into a database from which key insights are pulled to answer questions from the operations team. This project is deployed in four main milestones.

## Milestone 1
### Environment set up


A Python environment is created up in VScode, Jupyter notebook activated, GitBash is installed. Necessary libraries required for the project were installed as well. Vital libraries used include Numpy, Pandas, PyYAML, requests, SQLAlchemy, psycopg2, botocore, boto3, s3, tabula and their dependencies. Finally a Github repository was set up for version control and management and for the team to view project progress.

## Milestone 2
### Extract and Clean Data from different data sources


A PGAdmin4 database called sales_data is initialised locally to store extracted data.
Using Python scripts, files with classes and methods to extract data, clean it and upload the cleaned data to the database were created. 
  
1. **Extraction**


A data_extraction.py file handles all extraction of data. Its class named DataExtractor work as a utility class; in it methods that help extract data from different data sources were created. 
The methods include:
- **read_rds_table** It reads from RDS database through the engine. This starts a connection to a SQAlchemy engine to allow access to data from a sql table and returns a pandas DataFrame.
- **list_db_tables** It inspects the database for table names. This takes the engine as an argument and returns the table names.
- **retrieve_pdf_data** This retrieves pdf data from given AWS link. It enables data extraction from a PDF file on an Amazon AWS repository and contain store card details, it returns a pandas DataFrame named card_df.

(*A dictionary was created to provide details for 2 API endpoints, this is needed to create a method to return number of stores which another method will take in as argument to extract data from the number of stores*.)
- **list_number_of_stores** Method to list number of stores to retrieve data from, it returns a number.
- **retrieve_store_data** This method retrieves data of a number of stores from the given aws link and returns a pandas DataFrame.
- **extract_from_s3** This method extracts products_data csv file from an AWS S3 Bucket and returns a pandas DataFrame.
- **extract_json** This method gets a json file from an AWS s3 link and returns a pandas DataFrame.

2. **Connection**


Using Python script, a file named database_utils.py is created. Its class DatabaseConnector and methods are created to enable connection to and upload data to the empty database ceated in PGAdmin4. The methods include
- **read_db_creds** 
This method reads secured details on a yaml file required for connection through the sqlalchemy database engine to extract and through the engine to load to the database.
- **init_db_engine**
This method initialises and returns a sqlalchemy database engine. It takes the details from the yaml file and connects to the engine.
- **upload_to_db**
This function uses the engine to connect to the local postgresql database and uploads cleaned data.
    
3. **Cleaning** 


Finally, using Python script, a file named data_cleaning.py is created. It contain a class DataCleaning with methods to clean data from each of the data sources.
All methods defined in the cleaning process are explained in the data_cleaning.py file. Various data transform techniques in Pandas and Numpy were employed to remove erroneous data, duplicates, bad and null values. Users' data, stores' data, products' data, orders' and dates' data were processed. Dirty data is cleaned; nulls are removed as safely as possible while maintaining data integrity. Mathematical conversions are made in the conversion method for products data. Also data types were changed in some places to avoid bottlenecks in the future especially while doing data analysis. 

## Milestone 3
### Schema Development


After uploading the cleaned data to the sales_data database, a star-based schema is required to be developed. The generated postgresql tables were modified such that data types of some columns were cast into more appropriate datatypes. The **text** type of date column was changed to **dateuuid**, **text** type of product_quantity column changed to **smallint** and more. Certain updates were implemented across the tables; renaming some columns to match operational requirements, setting some conditions on products with SET and CASE statements for clearer identification and better user experience. 


To form the star-based schema, Primary keys and foreign keys constraints are set on appropriate columns. Certain corrections are required as some data cleansing methods may have chopped off some essential data. I had to make some 
error correction on products_data, orders_data and dates_data in VScode, checking for missing values, rewriting the codes and testing in Jupyter notebook then re-upload back to PgAdmin4 before attempting to add the foreign key constraints successfully. Some missing values were inserted with INSERT statements to fill in nulls created during JOINs.These are essential in aligning key columns in the dimensions table, the columns ids have to match in labels and data types. 

## Milestone 4
### Querying the Data


This section is mainly for data analysis. The Operations team has questions that need solutions from the derived data. There are nine key questions to which solutions are provided by using SQL syntaxes in DDL, DQL, and DML. The questions are answered as tasks.

Certain questions posed more challenge to me, out of which is Question 9: Determine the average time taken between each sale grouped by year.


The task is interpreted as finding the average of the time difference between each sale over the years. 
Average(sale timestamp - next sale timestamp) computed over the years and ordered by 
the average timestamp descending. The solution uses three CTEs to concatenate given time details to form a timestamp. SQL window function LEAD() returns the next record in the timestamp set in the next_times column.
The average times column is derived with the AVG() function used on the difference between sale 
Timestamps. Finally the required parameters are extracted from the average times. 
(Slight issue remains- milliseconds were hard to extract, there exist some negative values in the computations. I could ignore the milliseconds detail??!)



