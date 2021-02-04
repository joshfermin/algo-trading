from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import numpy as np
import pandas as pd
import datetime
import sys, getopt

from backtesting.test import SMA, GOOG

# imports for strategy, that may be removed when absracted out
from algo_trading.strategies.parabolic_sar import parabolic_sar
from algo_trading.strategies.rsi import rsi
from algo_trading.exchange.exchange_context import ExchangeContext
from algo_trading.exchange.robinhood_actions import RobinhoodActions

# 
# TODO: move this test strat out of her to make it more robust in taking an strats
# 
class PSAR_RSI(Strategy):

    def init(self, position = 0):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        self.p_sar = self.I(parabolic_sar, high, low, 0.01, 0.2)
        self.rsi = self.I(rsi, close)

    def next(self):
        latest_sar = self.p_sar[-1]
        latest_rsi = self.rsi[-1]
        current_bid_price = self.data.Close[-1]

        if(len(self.data.Close) > 336):
            if self.position.size <= 0 and current_bid_price > latest_sar and latest_rsi < 50:
                self.buy()
            elif self.position.size > 0 and current_bid_price < latest_sar and latest_rsi > 50 :
                self.position.close()
        
            relative_position = self.position.size if self.position.size >= 0 else 0
            print(  "total:", round(self.equity),
                    "units:", round(relative_position, 2),
                    "sar:", round(latest_sar, 2),
                    "rsi:", round(latest_rsi,2),
                    "bid_price:", round(current_bid_price, 2))


def backtest_our_fate(strat, ticker):
    exchange_actions = ExchangeContext(RobinhoodActions())
    crypto_historicals = exchange_actions.get_crypto_historicals(ticker, interval="hour", span="3month", bounds="24_7")

    # handle start and end day to find the corresponding indexes in historical crypto data
    start_date = datetime.datetime(2021, 1, 2).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date = datetime.datetime(2021, 1, 30).strftime("%Y-%m-%dT%H:%M:%SZ")
    start_date_index = [historical['begins_at'] for historical in crypto_historicals].index(start_date)
    end_date_index = [historical['begins_at'] for historical in crypto_historicals].index(end_date)

    # 336 hours is 14 days, we are taking 2 weeks af data before the first buy, and ending on the end day index
    historical_period = crypto_historicals[start_date_index-336:end_date_index]

    # get all relevant prices from the historical period above
    close_prices = np.asarray([float(historical['close_price']) for historical in historical_period])
    open_prices = np.asarray([float(historical['open_price']) for historical in historical_period])
    highs = np.asarray([float(historical['high_price']) for historical in historical_period])
    lows = np.asarray([float(historical['low_price']) for historical in historical_period])

    # format into pandas DataFrame format for ingestion into Backtest
    d = {'Open': open_prices, 'High': highs, 'Low':lows, 'Close': close_prices}
    d_formated = pd.DataFrame(data=d)

    bt = Backtest(d_formated, strat,
              cash=10000, commission=0.0,
              exclusive_orders=True, trade_on_close=True)

    # 
    # Outputs below
    # 
    output = bt.run()
    print('---------------------------------')
    print(output)
    print('---------------------------------')

    print(' ')
    print('IF THERE IS AN ERROR LIKE <The system cannot find the file specified.> AND YOU ARE USING WSL')
    print('DISREGARD, THIS IS FINE.... I THINK')

    # plot it up, plot it up
    bt.plot(filename="tests/plots/HEREWEGO.html")


backtest_our_fate(PSAR_RSI, "ETH")

