import time
import talib
import numpy as np
from algo_trading.enums import Decision
from algo_trading.strategies.base_strategy import BaseStrategy

class EMA(BaseStrategy):
    def __init__(self, period = 9):
        self.period = period
 
    def calculate(self, close_prices, term):
        return talib.EMA(close_prices, term)

    def indicators(self):
        return [
            {"name": f"ema" , "params": { "term": self.period }},
        ]
    
    def getDecision(self, params):
        ema = self.calculate(params['close'], self.period)

        if ema[-1] < params['close'][-1]:
            return Decision.BUY
        return Decision.SELL

ema = EMA