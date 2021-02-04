import time
import talib
import numpy as np

def rsi(prices):
    """RSI implementation. Pass in prices to return RSI calulations.

    Args:
        prices: A numpy array of floats representing prices over a time period.

    Returns:
        A numpy array. Each element represents the parabolicSAR calculation
    """
    return talib.RSI(prices)

# def evaluate_performance(latest_sar, current_bid_price, positions, position, bank_balance):
    # if(position == 0 and current_bid_price > latest_sar):
    #     position += positions
    #     bank_balance -= current_bid_price*positions
    # if(position > 0 and current_bid_price < latest_sar):
    #     position -= positions
    #     bank_balance += current_bid_price*positions
    # print("position:", position, "bank_balance:", bank_balance, "sar:", latest_sar, "bid_price:", current_bid_price)
    # return {
    #     "position": position,
    #     "bank_balance": bank_balance
    # }
