from algo_trading.strategies.sma import SMA

class SMACrossoverEvent(SMA):
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

sma_crossover_event = SMACrossoverEvent