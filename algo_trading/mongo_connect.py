from pymongo import MongoClient, DESCENDING
from algo_trading.settings import DB_CONNECTION_STRING

def mongo_client():
    connection_url = DB_CONNECTION_STRING
    return MongoClient(connection_url)

def historical_data_collection(symbol='ETH', time_interval='hour'):
    client = mongo_client()
    database = client.crypto
    collection = database[f'{symbol}_historical_data_{time_interval}_interval'.lower()]
    collection.create_index([('date', DESCENDING)], unique=True)
    return collection