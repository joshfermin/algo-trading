from pymongo import MongoClient
from algo_trading.settings import DB_CONNECTION_STRING

def mongo_client():
    connection_url = DB_CONNECTION_STRING
    return MongoClient(connection_url)

def historical_data_collection():
    client = mongo_client()
    database = client.okcoindb
    return database.historical_data

def rh_crypto_collection():
    client = mongo_client()
    database = client.rhdb
    return database.historical_data