import time
import talib
import numpy as np

class ParabolicSAR:
    def __init__(self, weight, acceleration=0.02, maximum=0.2):
        self.weight = weight
        self.acceleration = acceleration
        self.maximum = maximum

    """Parabolic SAR implementation. Pass in highs and lows to return SAR points.
    Args:
        highs: A numpy array of floats representing high prices over a time period.
        lows: A numpy array of floats representing low prices over a time period.
        n: An integer (180, 360, or 720) representing the length of time series.
    Returns:
        A numpy array. Each element represents the parabolicSAR calculation
    """
    def calcParabolicSAR(self, highs, lows):
        return talib.SAR(highs, lows, acceleration=self.acceleration, maximum=self.maximum)

    def getScore(self, price, highs, lows):
        sar = self.calcParabolicSAR(highs, lows)
        
        if price > sar[-1]:
            return 1 * self.weight
        elif price < sar[-1]:
            return -1 * self.weight
        return 0


def parabolic_sar(highs, lows, acceleration=0.02, maximum=0.2):
    """Parabolic SAR implementation. Pass in highs and lows to return SAR points.

    Args:
        highs: A numpy array of floats representing high prices over a time period.
        lows: A numpy array of floats representing low prices over a time period.
        n: An integer (180, 360, or 720) representing the length of time series.

    Returns:
        A numpy array. Each element represents the parabolicSAR calculation
    """
    return talib.SAR(highs, lows, acceleration=acceleration, maximum=maximum)

def evaluate_performance(latest_sar, current_bid_price, positions, position, bank_balance):
    if(position == 0 and current_bid_price > latest_sar):
        position += positions
        bank_balance -= current_bid_price*positions
    if(position > 0 and current_bid_price < latest_sar):
        position -= positions
        bank_balance += current_bid_price*positions
    print("position:", position, "bank_balance:", bank_balance, "sar:", latest_sar, "bid_price:", current_bid_price)
    return {
        "position": position,
        "bank_balance": bank_balance
    }
