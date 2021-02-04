import os
from dotenv import load_dotenv

load_dotenv()

DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

RH_USERNAME = os.getenv("RH_USERNAME")
RH_PASSWORD = os.getenv("RH_PASSWORD")
RH_TWO_FACTOR = os.getenv("RH_TWO_FACTOR")

ETRADE_KEY = os.getenv("ETRADE_KEY")
ETRADE_SECRET = os.getenv("ETRADE_SECRET")