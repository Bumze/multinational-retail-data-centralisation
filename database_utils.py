import pandas as pd
import yaml
import psycopg2
from sqlalchemy import create_engine

class DatabaseConnector:
    def __init__(self) -> None:
        pass

    def read_db_creds(self, filename):   
        with open (filename, 'r') as file:
            return yaml.safe_load(file)
        
    ''' This method initialises and returns a sqlalchemy database engine.  '''  
    def init_db_engine(self, creds): 
        engine = create_engine(f"postgresql://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}")
        engine.connect()
        return engine
    
    ''' function uses the engine to connect to the local postgres database and uploads cleaned data '''
    def upload_to_db(self, df, table_name, my_engine):
        creds = self.read_db_creds('local_db_creds.yaml')
        my_engine = create_engine(f"{'postgresql'}+{'psycopg2'}://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}")
        my_engine.connect()
        df.to_sql(table_name, my_engine, if_exists='replace')

if __name__=='__main__':
    databaseConnector = DatabaseConnector()

   