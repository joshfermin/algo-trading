import time
import talib
import numpy as np

import algo_trading.exchanges.robinhood_auth
import robin_stocks as r

from pytz import utc
from algo_trading.mongo_connect import rh_crypto_collection
from apscheduler.schedulers.blocking import BlockingScheduler

collection = rh_crypto_collection()

def get_last_n_ticks(num_ticks=8640):
    # Retrieve price, v_ask, and v_bid data points from the database.
    highs = []
    lows = []

    for doc in collection.find().sort('_id', -1).limit(num_ticks):
        highs.insert(0, float(doc['high']))
        lows.insert(0, float(doc['low']))
    
    return {
        'High': highs,
        'Low': lows
    }

def parabolic_sar():
    # loop or job?
    # First check current price above vwap or you have a position in the stock
    # if loop:
    # set position to 0 - can be 0, -1, or 1
    # while true

        # every 5 mins check close vs SAR
        # if close < SAR, buy signal
        # if close > SAR, sell signal
            # buy when sar switches form top to bottom
            # also put stop loss at SAR point (2% less)
    bank_balance = 0
    position = 0
    while True:
        data = get_last_n_ticks(10)
        bid_price = float(r.crypto.get_crypto_quote("BTC")['bid_price'])
        sar = talib.SAR(np.asarray(data['High']), np.asarray(data['Low']), acceleration=0.02, maximum=0.2)
        if(position == 0 and bid_price > sar[-1]):
            position += 1
            bank_balance -= bid_price
        if(position > 0 and bid_price < sar[-1]):
            position -= 1
            bank_balance += bid_price
        print("position:", position, "bank_balance:", bank_balance, "sar:", sar[-1], "bid_price:", bid_price)
        time.sleep(60)

def main():
    parabolic_sar()


if __name__ == '__main__':
    main()