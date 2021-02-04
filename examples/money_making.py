import time
import numpy as np

from pymongo import MongoClient
from algo_trading.strategies.parabolic_sar import *
from algo_trading.exchange.exchange_context import ExchangeContext
from algo_trading.exchange.robinhood_actions import RobinhoodActions

def test_strategy(interval, exchange_actions, symbol):
    bank_balance = 0
    position = 0
    
    while True: 
        crypto_historicals = exchange_actions.get_crypto_historicals(symbol, interval="5minute", span="day", bounds="24_7")

        highs = np.asarray([float(historical['high_price']) for historical in crypto_historicals])
        lows = np.asarray([float(historical['low_price']) for historical in crypto_historicals])

        sar = parabolic_sar(highs, lows)

        performance = evaluate_performance(sar[-1], float(exchange_actions.get_crypto_quote(symbol)['bid_price']), 300, position, bank_balance)
        bank_balance = performance['bank_balance']
        position = performance['position']
        time.sleep(interval)

test_strategy(300, ExchangeContext(RobinhoodActions()), "ETH")