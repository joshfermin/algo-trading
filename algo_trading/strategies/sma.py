import time
import talib
import numpy as np
from algo_trading.enums import Decision

class SMA:
    def __init__(self, longer = 200, shorter = 100):
        self.longer = longer
        self.shorter = shorter

    """SMA implementation. Pass in prices to return SMA calulations.
    Args:
        prices: A numpy array of floats representing prices over a time period.
        term: MA length term
    Returns:
        A numpy array. Each element represents the parabolicSAR calculation
    """
    def calculate(self, close_prices, term):
        return talib.SMA(close_prices, term)

    def indicators(self):
        return [
            {"name": f"sma_short" , "params": { "term": self.shorter }},
            {"name": f"sma_long" , "params": { "term": self.longer }}
        ]
    
    def getDecision(self, params):
        sma_long = self.calculate(params['close'], self.longer)
        sma_short = self.calculate(params['close'], self.shorter)

        if sma_long[-1] < sma_short[-1]:
            return Decision.BUY
        elif sma_long[-1] > sma_short[-1]:
            return Decision.SELL
        return Decision.NOOP

sma = SMA