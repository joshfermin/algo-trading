import time
import talib
import numpy as np
from algo_trading.enums import Decision

class SMA:
    def __init__(self, params={"longer": 200, "shorter": 100}):
        self.longer = params["longer"]
        self.shorter = params["shorter"]

    """SMA implementation. Pass in prices to return SMA calulations.
    Args:
        prices: A numpy array of floats representing prices over a time period.
        term: MA length term
    Returns:
        A numpy array. Each element represents the parabolicSAR calculation
    """
    def calcSMA(self, prices, term):
        return talib.SMA(prices, term)
    
    def getScore(self, prices):
        sma_long = self.calcSMA(prices, self.longer)
        sma_short = self.calcSMA(prices, self.shorter)

        if sma_long[-1] < sma_short[-1]:
            return Decision.BUY
        elif sma_long[-1] > sma_short[-1]:
            return Decision.SELL
        return Decision.NOOP

sma = SMA