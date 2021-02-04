import time
import numpy as np
import requests
import datetime

from pymongo import MongoClient
from algo_trading.strategies.parabolic_sar import parabolic_sar
from algo_trading.strategies.rsi import rsi
from algo_trading.exchange.exchange_context import ExchangeContext
from algo_trading.exchange.robinhood_actions import RobinhoodActions


def evaluate_performance(latest_sar, latest_rsi, current_bid_price, allin, position, bank_balance):
    # seems like 50 is sweet spot for rsi, can't be too strict because it will never buy or sell, as crypto is too volatile
    if(position == 0 and current_bid_price > latest_sar and latest_rsi < 50):
        buy_amount = int(bank_balance/current_bid_price) if allin else 1
        position += buy_amount
        bank_balance -= current_bid_price*buy_amount
    if(position > 0 and current_bid_price < latest_sar and latest_rsi > 50):
        bank_balance += current_bid_price*position
        position -= position
    
    print("total:", round(bank_balance + current_bid_price*position, 2) , "units:", round(position, 2), "sar:", round(latest_sar, 2), "rsi:", round(latest_rsi,2), "bid_price:", round(current_bid_price, 2))
    return {
        "position": position,
        "bank_balance": bank_balance
    }

# basically a test/sandbox with previous data
def what_i_could_have_become_hour_3month():
    exchange_actions = ExchangeContext(RobinhoodActions())

    bank_balance = 10000
    position = 0
    start_date = datetime.datetime(2021, 1, 2).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date = datetime.datetime(2021, 1, 30).strftime("%Y-%m-%dT%H:%M:%SZ")

    crypto_historicals = exchange_actions.get_crypto_historicals("ETH", interval="hour", span="3month", bounds="24_7")

    start_date_index = [historical['begins_at'] for historical in crypto_historicals].index(start_date)
    end_date_index = [historical['begins_at'] for historical in crypto_historicals].index(end_date)

    pointer = start_date_index

    while pointer != end_date_index: 
        # two weeks of data from for parabolic sar to analyze
        historical_period = crypto_historicals[pointer-336:pointer+1]

        prices = np.asarray([float(historical['close_price']) for historical in historical_period])
        highs = np.asarray([float(historical['high_price']) for historical in historical_period])
        lows = np.asarray([float(historical['low_price']) for historical in historical_period])

        sar = parabolic_sar(highs, lows, 0.01, 0.2)

        rsi_calc = rsi(prices)

        performance = evaluate_performance(sar[-1], rsi_calc[-1], float(historical_period[-1]['close_price']), True, position, bank_balance)
        bank_balance = performance['bank_balance']
        position = performance['position']

        pointer += 1
        

what_i_could_have_become_hour_3month()


# big yikes
# def what_i_could_have_become_10min_week():
#     exchange_actions = ExchangeContext(RobinhoodActions())

#     bank_balance = 50000
#     position = 0
#     start_date = datetime.datetime(2021, 1, 30).strftime("%Y-%m-%dT%H:%M:%SZ")
#     end_date = datetime.datetime(2021, 2, 3).strftime("%Y-%m-%dT%H:%M%SZ")

#     crypto_historicals = exchange_actions.get_crypto_historicals("ETH", interval="10minute", span="week", bounds="24_7")

#     start_date_index = [historical['begins_at'] for historical in crypto_historicals].index(start_date)
#     end_date_index = [historical['begins_at'] for historical in crypto_historicals].index(end_date)

#     pointer = start_date_index
    
#     # pointer_back = 336
#     # pointer_back = 30
#     pointer_back = 200

#     while pointer != end_date_index: 
#         historical_period = crypto_historicals[pointer-pointer_back:pointer+1]

#         highs = np.asarray([float(historical['high_price']) for historical in historical_period])
#         lows = np.asarray([float(historical['low_price']) for historical in historical_period])

#         sar = parabolic_sar(highs, lows)

#         performance = evaluate_performance(sar[-1], float(historical_period[-1]['close_price']), 1, position, bank_balance)
#         bank_balance = performance['bank_balance']
#         position = performance['position']

#         pointer += 1
        

# what_i_could_have_become_10min_week()


# original test strat
def test_strategy(interval):
    exchange_actions = ExchangeContext(RobinhoodActions())

    bank_balance = 3000
    position = 1
    
    while True: 
        crypto_historicals = exchange_actions.get_crypto_historicals("ETH", interval="5minute", span="week", bounds="24_7")

        highs = np.asarray([float(historical['high_price']) for historical in crypto_historicals])
        lows = np.asarray([float(historical['low_price']) for historical in crypto_historicals])

        sar = parabolic_sar(highs, lows)

        performance = evaluate_performance(sar[-1], float(exchange_actions.get_crypto_quote("ETH")['bid_price']), 300, position, bank_balance)
        bank_balance = performance['bank_balance']
        position = performance['position']
        time.sleep(interval)

# test_strategy(300)