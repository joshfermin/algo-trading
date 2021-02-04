from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG

import numpy as np
import pandas as pd
from algo_trading.exchange.exchange_context import ExchangeContext
from algo_trading.exchange.robinhood_actions import RobinhoodActions

# sample tests from the online docs
class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        print(self.position.size)
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()

# start of custom crypto data
exchange_actions = ExchangeContext(RobinhoodActions())
crypto_historicals = exchange_actions.get_crypto_historicals("ETH", interval="hour", span="3month", bounds="24_7")

period_historicals = crypto_historicals[1300:]

close_prices = np.asarray([float(historical['close_price']) for historical in period_historicals])
open_prices = np.asarray([float(historical['open_price']) for historical in period_historicals])
highs = np.asarray([float(historical['high_price']) for historical in period_historicals])
lows = np.asarray([float(historical['low_price']) for historical in period_historicals])

d = {'Open': open_prices, 'High': highs, 'Low':lows, 'Close': close_prices}
df = pd.DataFrame(data=d)
# end of custom crypto data

bt = Backtest(GOOG, SmaCross,
              cash=10000, commission=.000,
              exclusive_orders=True)

output = bt.run()
print('---------------------------------')
print(output)
print('---------------------------------')
bt.plot(filename="tests/plots/TEST.html")