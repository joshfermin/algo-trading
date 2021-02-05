import time
import talib
import numpy as np

class RSI:
    def __init__(self, weight, high=70, low=30):
        self.weight = weight
        self.high = high
        self.low = low

    """RSI implementation. Pass in prices to return RSI calulations.
    Args:
        prices: A numpy array of floats representing prices over a time period.
    Returns:
        A numpy array. Each element represents the parabolicSAR calculation
    """
    def calcRSI(self, prices):
        return talib.RSI(prices)

    def getScore(self, prices):
        rsi = self.calcRSI(prices)
        
        if rsi[-1] < self.low:
            # buy
            # score_plus = abs(np.log((self.low -rsi[-1])/self.low) / 4)
            score_plus = 0
            # print((1 + score_plus) * self.weight)
            return (1 + score_plus) * self.weight
        elif rsi[-1] > self.high:
            # sell
            # score_plus = abs(np.log(((100-self.high) - rsi[-1])/(100-self.high))/ 4)
            score_plus = 0
            return (-1 - score_plus) * self.weight
        return 0


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
