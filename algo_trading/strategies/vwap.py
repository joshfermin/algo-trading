import time
import talib
import numpy as np
from algo_trading.enums import GatedDecision
from algo_trading.strategies.base_strategy import BaseStrategy

class VWAP(BaseStrategy):
    def calculate(self, close_prices, volumes):
        return (np.cumsum(volumes * close_prices) / np.cumsum(volumes))

    def indicators(self):
        return [
            {"name": "vwap"},
        ]
    
    def getDecision(self, params):
        vwap = self.calculate(params['close'], params['volume'])

        if params['close'][-1] > vwap[-1]:
            return GatedDecision.CAN_HOLD_LONG_POSITION
        return GatedDecision.CAN_HOLD_SHORT_POSITION

vwap = VWAP