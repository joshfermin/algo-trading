from pymongo import MongoClient
from dotenv import load_dotenv
from bitcoin_price_prediction.settings import DB_CONNECTION_STRING

def mongo_client():
    connection_url = DB_CONNECTION_STRING
    return MongoClient(connection_url)

def historical_data_collection():
    client = mongo_client()
    database = client.okcoindb
    return database.historical_data