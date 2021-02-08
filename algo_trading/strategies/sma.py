import time
import talib
import numpy as np

class SMA:
    def __init__(self, weight, longer=200, shorter=50 ):
        self.weight = weight
        self.longer = longer
        self.shorter = shorter

    """SMA implementation. Pass in prices to return SMA calulations.
    Args:
        prices: A numpy array of floats representing prices over a time period.
        term: MA length term
    Returns:
        A numpy array. Each element represents the parabolicSAR calculation
    """
    def calcSMA(self, prices, term):
        return talib.SMA(prices, term)


class SMA_CROSSOVER_TREND(SMA):

    def getScore(self, prices):
        sma_long = self.calcSMA(prices, self.longer)
        sma_short = self.calcSMA(prices, self.shorter)

        if sma_long[-1] < sma_short[-1]:
            # buy
            # score_plus = abs(np.log((self.low -rsi[-1])/self.low) / 4)
            score_plus = 0
            # print((1 + score_plus) * self.weight)
            return (1 + score_plus) * self.weight
        elif sma_long[-1] > sma_short[-1]:
            # sell
            # score_plus = abs(np.log(((100-self.high) - rsi[-1])/(100-self.high))/ 4)
            score_plus = 0
            return (-1 - score_plus) * self.weight
        return 0


class SMA_CROSSOVER_EVENT(SMA):

    def getScore(self, prices):
        sma_long = self.calcSMA(prices, self.longer)
        sma_short = self.calcSMA(prices, self.shorter)

        if sma_long[-2] > sma_short[-2] and sma_long[-1] < sma_short[-1]:
            # buy when short crosses above long
            # score_plus = abs(np.log((self.low -rsi[-1])/self.low) / 4)
            score_plus = 0
            # print((1 + score_plus) * self.weight)
            return (1 + score_plus) * self.weight
        elif sma_long[-2] < sma_short[-2] and sma_long[-1] > sma_short[-1]:
            # sellwhen short crosses under long
            # score_plus = abs(np.log(((100-self.high) - rsi[-1])/(100-self.high))/ 4)
            score_plus = 0
            return (-1 - score_plus) * self.weight
        return 0.1 * self.weight
