from pandas import DataFrame
from algo_trading.enums import Decision
from algo_trading.strategies.base_strategy import BaseStrategy

class IchimokuCloud(BaseStrategy):
    def calculate(self, highs, lows, close_prices, span=None):
        highs = DataFrame(highs,columns=['High'])
        lows = DataFrame(lows,columns=['Low'])
        close_prices = DataFrame(close_prices, columns=['Close'])

        data = {}

        high_9 = highs.High.rolling(9).max()
        low_9 = lows.Low.rolling(9).min()
        data['tenkan_sen_line'] = (high_9 + low_9) /2
        # Calculate Kijun-sen
        high_26 = highs.High.rolling(26).max()
        low_26 = lows.Low.rolling(26).min()
        data['kijun_sen_line'] = (high_26 + low_26) / 2
        # Calculate Senkou Span A
        data['senkou_span_A'] = ((data['tenkan_sen_line'] + data['kijun_sen_line']) / 2).shift(26)
        # Calculate Senkou Span B
        high_52 = highs.High.rolling(52).max()
        low_52 = highs.High.rolling(52).min()
        data['senkou_span_B'] = ((high_52 + low_52) / 2).shift(26)
        # Calculate Chikou Span B
        data['chikou_span'] = close_prices.Close.shift(-26)

        if span != None:
            return data[span]

        return data

    def indicators(self):
        return [
            {"name": "senkou_span_a", "params": { "span": "senkou_span_A" } },
            {"name": "senkou_span_b", "params": { "span": "senkou_span_B" } }
        ]

    def getDecision(self, params):
        price = params['close'][-1]
        data = self.calculate(params['high'], params['low'], params['close'], None)
        
        if price > data['senkou_span_A'].values[-1] and price > data['senkou_span_B'].values[-1]:
            return Decision.BUY
        elif price < data['senkou_span_A'].values[-1] and price < data['senkou_span_B'].values[-1]:
            return Decision.SELL
        return Decision.NOOP

ichimoku_cloud = IchimokuCloud
