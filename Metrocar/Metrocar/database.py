import sqlalchemy as sa
from sqlalchemy import create_engine, text
import pandas as pd
from flask import current_app
import pg8000

DATABASE_URI = "postgresql+pg8000://Test:bQNxVzJL4g6u@ep-noisy-flower-846766-pooler.us-east-2.aws.neon.tech/Metrocar"

engine = None
connection = None

def get_table_names ():    
    init_engine()
    inspector = sa.inspect(engine)
    return inspector.get_table_names()

def init_engine ():
    global engine
    if engine is None:
        engine = create_engine(DATABASE_URI)
        
def get_connection():    
    global connection, engine
    init_engine ()    
    if connection is None:
        try:
            connection = engine.connect()
            print("Database connection established.")
        except Exception as e:
            print(f"Error establishing database connection: {e}")
    return connection

data_dictionary = {}

def is_running_locally():    
    return current_app.debug

    
def load_data_locally():
     
     table_names = ["app_downloads", "ride_requests", "reviews", "signups", "transactions"]
     for table_name in table_names:
        try:    
            if table_name in data_dictionary:
                continue
            print(f"Loading... {table_name}:") 
            data_dictionary[table_name] = pd.read_csv(f'{table_name}.csv')           
        except Exception as e:
            print(f"Error loading data for table '{table_name}': {e}")


def load_data(table_name):    
    try:
        if is_running_locally():
            load_data_locally()
        if table_name in data_dictionary:
            return data_dictionary[table_name]
        print (f"Loading...{table_name}")
        data_dictionary[table_name] = pd.read_sql(table_name, get_connection())        
        print ("Loaded")
        return data_dictionary[table_name]
    except Exception as e:
        print(f"Error loading data from {table_name}: {e}")
        return pd.DataFrame() 

all_data = None

def merge_data ():
    global all_data

    print ('merging app_downloads with signups...')
    all_data = pd.merge (left=data_dictionary['app_downloads'], 
                 right=data_dictionary['signups'], 
                 how="left", left_on="app_download_key", right_on="session_id")
    print ('merging with ride_requests...')
    all_data = pd.merge (left=all_data, 
                         right=data_dictionary['ride_requests'], 
                         how="left", on="user_id")
    print ('merging with transactions...')
    all_data = pd.merge (left=all_data, 
                         right=data_dictionary['transactions'], 
                         how="left", on="ride_id")
    print ('merging with reviews...')
    all_data = pd.merge (left=all_data, right=data_dictionary['reviews'], 
                         how="left", on="ride_id")
    
    print ('creating  signedup_users...')    
    all_data['signedup_users'] = all_data['user_id_x'].notnull()
    print ('creating  ride_request...')  
    all_data['ride_request'] = all_data['request_ts'].notnull()
    print ('creating  ride_finished...')  
    all_data['ride_finished'] = all_data['dropoff_ts'].notnull() &  all_data['cancel_ts'].isnull()
    print ('creating  ride_paid...')  
    all_data['ride_paid'] = all_data['charge_status'] == 'Approved'
    print ('creating  ride_reviewed...')  
    all_data['ride_reviewed'] = all_data['review_id'].notnull()
    return all_data