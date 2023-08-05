import pandas as pd
import numpy as np
import re

class DataCleaning:
    def __init__(self) -> None:
        pass

    def clean_user_data(self, user_df):

        '''A method created to clean user data. It takes user_df as a parameter, replaces null values with numpy NaN and drops them.
          It changes data types of columns 'date_of_birth' and 'join_date' then removes all unwanted characters from various columns.
          Column 'phone_number' is rearranged to Telecommunications regular codeformat- intl' 'country' 'state/mobile' 'lastsevendigit. 
          Duplicate indexes dropped and index reset. It returns user_df dataframe.'''
        
        user_df = user_df.replace('NULL', np.nan)
        user_df = user_df.dropna(how='any')
        user_df[['date_of_birth', 'join_date']] = user_df[['date_of_birth', 'join_date']].apply(lambda x: pd.to_datetime(x, format='%Y-%m-%d' , errors='coerce'))
        user_df['email_address'] = user_df['email_address'].str.replace('@@', '@')
        user_df['country_code'] = user_df['country_code'].str.replace('GG', 'G')
        user_df = user_df[~(user_df.country_code.str.len() > 3)] 
        user_df['phone_number'] = user_df['phone_number'].str.replace('x','').str.replace('+','00').replace('[^a-zA-Z0-9]','', regex=True)
        user_df['phone_number'] = user_df['phone_number'].apply(lambda x:x[0:4]+ ' '+ x[4:8]+' ' + x[-7:-4] +' ' + x[-4:] if len(x)>11 else x[0:4]+ ' ' + x[-7:-4] +' ' + x[-4:])
        user_df = user_df.set_index(user_df.columns[0])
        user_df = user_df.reset_index(drop=True)
        return user_df

    def clean_store_data(self, stores_df):

        '''replaces null values with numpy nan,  checks if the index of the column 'index' is in the listed, 
        if so drop the rows with the listed indexes. It drops the null lat column and rows with NaN values,
        then replaces 'ee' in eeEurope and eeAmerica. Finally it drops duplicate 'index' and 'Unnamed' colunms 
        then reset index while it returns stores_df dataframe.'''


        stores_df = stores_df.replace('NULL', np.nan)
        bad_rows = stores_df['country_code'][stores_df['country_code'].str.len() > 3].index # get indexes for which month values>3
        stores_df = stores_df.drop(bad_rows)# drop the bad rows
        stores_df = stores_df.dropna(how='all', axis=0)
        stores_df = stores_df.drop('lat', axis = 1)
        stores_df['continent'] = stores_df['continent'].str.replace('ee ', '')
        stores_df = stores_df.loc[stores_df['country_code'].isin(['GB', 'US', 'DE'])]
        stores_df['opening_date'] = pd.to_datetime(stores_df ['opening_date'], errors ='coerce')
        stores_df['staff_numbers'] = stores_df['staff_numbers'].astype('str').apply(lambda x : re.sub('\D','',x))
        stores_df = stores_df.set_index(stores_df.columns[0])
        stores_df = stores_df.reset_index(drop=True)
        return stores_df

    def clean_card_data(self, card_df):
        '''A method created to clean card data. It takes card_df as a parameter, enforces card number column 
        values are digits while provider column is text without 'digit'. It changes dates dtype to datetime, 
        duplicate columns dropped and index reset. It returns card_df dataframe.'''
        card_df = card_df.drop_duplicates(keep='first')
        card_df = card_df[card_df['card_number'].apply(lambda x: str(x).isdigit())]
        card_df['card_provider'] = card_df['card_provider'].apply(lambda x: re.sub(r"\d+", "", x)).str.strip('digit')
        card_df['date_payment_confirmed'] = pd.to_datetime(card_df['date_payment_confirmed'], errors='coerce') 
        card_df.dropna(inplace=True)
        card_df = card_df.reset_index(drop=True)
        return card_df
    
    def convert_product_weights(self, x): 
        
        '''A method created to convert units of weights->'x', strips the units 
        and returns the output as a float type.'''

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
        '''A method created to clean products data. It takes product_df as a parameter,
        it replaces null values with NaN and NaT then drops rows wth any of them.It also
        drops bad rows identified with longer values in 'product_price' column. Rows with values 
        longer than average length in 'product_price' are dropped.
        The method changes dates dtype to datetime, price to float and some dtype objects to category. 
        Duplicate columns dropped and index resetIt returns products_df dataframe. '''

        products_df = products_df.replace('NULL', np.nan)
        products_df = products_df[~products_df.isin(['NaN', 'NaT']).any(axis=1)]
        products_df = products_df.dropna(how='any', axis=0)
        products_df =  products_df.copy()# overcome chained reassignment 
        products_df['date_added'] = pd.to_datetime(products_df['date_added'], errors ='coerce')
        products_df = products_df[~(products_df.product_price.str.len() > 8)] 
        products_df['weight'] = products_df['weight'].apply(self.convert_product_weights)
        products_df['weight'] = products_df['weight'].astype('float')
        products_df['product_price'] = products_df['product_price'].apply(lambda x:str(x).strip('£'))
        products_df['product_price'] = products_df['product_price'].astype('float')
        products_df['category'] = products_df['category'].astype('category')
        products_df['removed'] = products_df['removed'].astype('category')
        products_df = products_df.drop(products_df.columns[:1], axis = 1)
        products_df = products_df.reset_index(drop=True)
        return products_df
    
    def clean_orders_data(self, orders_df):
        '''A method created to clean orders data. It takes  orders_df as a parameter, it
        drops duplicate columns, set index as column 1 and resets. It returns orders_df dataframe.'''
        orders_df = orders_df.drop(orders_df[['first_name', 'last_name', '1']], axis=1)
        orders_df= orders_df.drop(orders_df.columns[:1], axis = 1)
        orders_df = orders_df.set_index(orders_df.columns[0])
        orders_df = orders_df.reset_index(drop=True)
        return orders_df

    def clean_dates_data(self, dates_df):
        '''A method created to clean dates details. It takes dates_df as a parameter, 
        it creates bad rows using len() on 'month' column, drops the bad rows and 
        resets index. It returns dates_df dataframe.'''
        bad_rows = dates_df['month'][dates_df['month'].astype(str).str.len() > 3].index # get indexes for which month values>3
        dates_df = dates_df.drop(bad_rows)# drop the bad rows
        dates_df = dates_df.reset_index(drop=True)
        return dates_df

if __name__ == '__main__':
    dataCleaning = DataCleaning()
