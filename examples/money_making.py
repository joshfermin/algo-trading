from pymongo import MongoClient
from algo_trading.strategies.parabolic_sar import *
from algo_trading.mongo_connect import historical_data_collection

import time
import numpy as np
import algo_trading.exchanges.robinhood_auth
import robin_stocks as r

def test_strategy(interval):
    bank_balance = 0
    position = 0
    
    while True: 
        crypto_historicals = r.get_crypto_historicals("BTC", interval="5minute", span="day", bounds="24_7")

        highs = np.asarray([float(historical['high_price']) for historical in crypto_historicals])
        lows = np.asarray([float(historical['low_price']) for historical in crypto_historicals])

        sar = parabolic_sar(highs, lows)

        performance = evaluate_performance(sar[-1], float(r.crypto.get_crypto_quote("BTC")['bid_price']), 300, bank_balance, position)
        bank_balance = performance['bank_balance']
        position = performance['position']
        time.sleep(interval)

test_strategy(300)