import time
import talib
import numpy as np

from algo_trading.enums import Decision
class RSI:
    def __init__(self, high=70, low=30):
        self.high = high
        self.low = low

    """RSI implementation. Pass in prices to return RSI calulations.
    Args:
        prices: A numpy array of floats representing prices over a time period.
    Returns:
        A numpy array. Each element represents the parabolicSAR calculation
    """
    def calculate(self, close_prices):
        return talib.RSI(close_prices)

    def indicators(self):
        return [{"name": "rsi"}]

    def getDecision(self, params):
        rsi = self.calculate(params['close'])
        
        if rsi[-1] < self.low:
            return Decision.BUY
        elif rsi[-1] > self.high:
            return Decision.SELL
        return Decision.NOOP

rsi = RSI