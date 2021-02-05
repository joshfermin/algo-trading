from pandas import DataFrame

def ichimoku_cloud(highs, lows, close_prices):
    highs = DataFrame(highs,columns=['High'])
    lows = DataFrame(lows,columns=['Low'])
    close_prices = DataFrame(close_prices,columns=['Close'])

    data = {}

    # TODO: make these use numpy instead so we dont need pandas
    # Calculate Tenkan-sen
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

    return data