import pandas as pd
import yaml
import psycopg2
from sqlalchemy import create_engine

class DatabaseConnector:
    def __init__(self) -> None:
        pass

    '''This method reads the credentials from yaml'''
    # def read_db_creds(self):
    #     with open ('db_creds.yaml', 'r') as file:
    #         return yaml.safe_load(file)

    def read_db_creds(self, filename):   
        with open (filename, 'r') as file:
            return yaml.safe_load(file)
        
    ''' This method initialises and returns a sqlalchemy database engine.  '''  
    def init_db_engine(self, creds): 
        # creds = self.read_db_creds() 
        engine = create_engine(f"postgresql://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}")
        engine.connect()
        return engine
    
    ''' function uses the engine to connect to the local postgres database and uploads cleaned data '''
    def upload_to_db(self, df, table_name, my_engine):
        creds = self.read_db_creds()
        my_engine = create_engine(f"{'postgresql'}+{'psycopg2'}://{creds['LOCAL_USER']}:{creds['PASSWORD']}@{creds['LOCAL_HOST']}:{creds['LOCAL_PORT']}/{creds['LOCAL_DATABASE']}")
        my_engine.connect()
        df.to_sql(table_name, my_engine, if_exists='replace')

if __name__=='__main__':
    databaseConnector = DatabaseConnector()

   