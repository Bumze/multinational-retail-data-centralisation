import pandas as pd
import numpy as np
import re

class DataCleaning:
    def __init__(self) -> None:
        pass

    def clean_store_data(self, stores_df):
        '''replaces null values with numpy nan,  
        check if the index of the column 'index' is in the listed, if so drop the rows with the listed indexes.
        drops 3 rows with NaN values, replace eeEurope and eeAmerica. 
        drop duplicate 'index' and incomplete 'lat' colunms'''
        
        stores_df = stores_df.replace('NULL', np.nan)
        stores_df = stores_df.drop(stores_df.index[stores_df['index'].isin([63,172,231,333,381,405,414,447])])# drop rows with bad data
        stores_df= stores_df.dropna(how='all')
        stores_df['continent'] = stores_df['continent'].str.replace('ee', '')
        stores_df['opening_date'] = pd.to_datetime(stores_df ['opening_date'], errors ='coerce')
        stores_df = stores_df.drop(['lat','index'], axis=1)
        stores_df = stores_df.reset_index(drop=True)
        return stores_df

    def clean_card_data(self, card_df):
        card_df = card_df.drop_duplicates(keep='first')
        card_df = card_df[card_df['card_number'].apply(lambda x: str(x).isdigit())]
        card_df['card_provider'] = card_df['card_provider'].apply(lambda x: re.sub(r"\d+", "", x)).str.strip('digit')
        card_df['date_payment_confirmed'] = pd.to_datetime(card_df['date_payment_confirmed'], errors='coerce') 
        card_df.dropna(inplace=True)
        card_df = card_df.reset_index(drop=True)
        return card_df
    
    def convert_product_weights(self, x):
        if 'kg' in str(x):
            x = x.strip('kg') 
            x = float(x)    
        elif 'ml' in str(x):
            x = x.replace('ml', '')
            x = float(x)/1000
        elif 'g' in str(x):
            x = x.replace(' ','')
            x = x.replace('g','')
            x = x.replace('x','*')
            x = eval(x)
            x = float(x)/1000 
        elif 'lb' in str(x):
            x = x.replace('lb', '')
            x = float(x)*0.453592
        elif 'oz' in str(x):
            x = x.replace('oz', '')
            x = float(x)*0.0283495  
        return x

    def clean_products_data(self, products_df):
        products_df['date_added'] = pd.to_datetime(products_df['date_added'], errors ='coerce')
        products_df = products_df[~(products_df.product_price.str.len() > 8)] 
        products_df['weight'] = products_df['weight'].apply(self.convert_product_weights)
        products_df['weight'] = products_df['weight'].astype('float')
        products_df['product_price'] = products_df['product_price'].apply(lambda x:str(x).strip('£'))
        products_df['product_price'] = products_df['product_price'].astype('float')
        products_df['category'] = products_df['category'].astype('category')
        products_df['removed'] = products_df['removed'].astype('category')
        cols = [0, 1] #why?->  forces df.columns to work as it threw an error initially
        products_df.drop(products_df.columns[cols], axis=1, inplace=True)
        products_df = products_df.reset_index(drop=True)
        return products_df
    
    def clean_orders_data(self, orders_df):
       orders_df.drop(['first_name', 'last_name', '1'], axis=1, inplace=True)
       return orders_df

if __name__ == '__main__':
    dataCleaning = DataCleaning()

