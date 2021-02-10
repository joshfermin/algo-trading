import time
import talib
import numpy as np

from algo_trading.enums import Decision

class ParabolicSAR():
    def __init__(self, params={"acceleration": 0.02, "maximum": 0.2}):
        self.acceleration = params['acceleration']
        self.maximum = params['maximum']

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

    def getDecision(self, params):
        price = params['close'][-1]
        sar = self.calcParabolicSAR(params['high'], params['low'])
        
        if price > sar[-1]:
            return Decision.BUY
        elif price < sar[-1]:
            return Decision.SELL
        return Decision.NOOP

parabolic_sar = ParabolicSAR
