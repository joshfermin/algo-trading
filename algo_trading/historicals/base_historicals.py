import numpy as np
import pandas as pd
from abc import abstractmethod, ABC

class BaseHistoricals(ABC):
    @abstractmethod
    def get_crypto_historicals(self, symbol, interval, span):
        pass

    def normalize_historicals_for_backtest(self, symbol, interval, span):
        historical_period = self.get_crypto_historicals(symbol, interval, span)

        close_prices = np.asarray([historical['close_price'] for historical in historical_period])
        open_prices = np.asarray([historical['open_price'] for historical in historical_period])
        highs = np.asarray([historical['high_price'] for historical in historical_period])
        lows = np.asarray([historical['low_price'] for historical in historical_period])
        dates = np.asarray([historical['date'] for historical in historical_period])
        volumes = np.asarray([historical['volume'] for historical in historical_period])

        # format into pandas DataFrame format for ingestion into Backtest
        d = {'Open': open_prices, 'High': highs, 'Low':lows, 'Close': close_prices, 'Volume': volumes, 'Datetime': dates}
        d_formated = pd.DataFrame(data=d)
        d_formated.set_index(pd.DatetimeIndex(d['Datetime']), inplace=True)
        return d_formated