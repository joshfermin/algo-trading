from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import numpy as np
import pandas as pd
import datetime
import sys, getopt
import statistics
import os
import dateutil.parser

from backtesting.test import SMA, GOOG
from algo_trading.enums import Decision

# imports for strategy, that may be removed when absracted out
from algo_trading.strategies.parabolic_sar import parabolic_sar, ParabolicSAR
from algo_trading.strategies.rsi import rsi, RSI
from algo_trading.strategies.stop_loss import StopLoss
from algo_trading.strategies.sma import sma
from algo_trading.strategies.strategy_mediator import StrategyMediator
from algo_trading.exchange.exchange_context import ExchangeContext
from algo_trading.exchange.robinhood_actions import RobinhoodActions
from utils.time import handle_time_period
from utils.args import get_config_from_args

# move to utils
import decimal

def float_range(start, stop, step):
    while start < stop:
        yield float(start)
        start += decimal.Decimal(step)


# 
# TODO: move this test strat out of her to make it more robust in taking an strats
# 
class THE_VERSION_WE_CALL_ONE(Strategy):
    def init(self, position = 0):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        self.mediator = StrategyMediator(config, for_backtesting=True, backtesting_instance=self)
        self.mediator.setup_indicators(self, high, low, close)

    def next(self):
        current_bid_price = self.data.Close[-1]

        if(len(self.data.Close) > 100):
            decision = self.mediator.decide({"high": self.data.High, "low": self.data.Low, "close": self.data.Close})
            
            if self.position.size <= 0 and decision == Decision.BUY.value:
                self.buy()
            elif self.position.size > 0 and decision == Decision.SELL.value:
                self.position.close()

            relative_position = self.position.size if self.position.size >= 0 else 0
            # print(  "total:", round(self.equity),
            #         "units:", round(relative_position, 2),
            #         # "sar:", round(latest_sar, 2),
            #         # "rsi:", round(latest_rsi,2),
            #         "bid_price:", round(current_bid_price, 2))


def backtest_our_fate(strat, config):
    ticker = config['symbol']
    cash = config['cash']
    interval = config['historicals']['interval']
    span = config['historicals']['span']

    start_date = None
    end_date = None
    exchange_actions = ExchangeContext(RobinhoodActions())
    crypto_historicals = exchange_actions.get_crypto_historicals(ticker, interval=interval, span=span, bounds="24_7")

    start_date = datetime.datetime(2021, 1, 2)
    end_date = datetime.datetime(2021, 2, 6)

    historical_period = handle_time_period(crypto_historicals, start_date, end_date, 100)

    # get all relevant prices from the historical period above
    close_prices = np.asarray([float(historical['close_price']) for historical in historical_period])
    open_prices = np.asarray([float(historical['open_price']) for historical in historical_period])
    highs = np.asarray([float(historical['high_price']) for historical in historical_period])
    lows = np.asarray([float(historical['low_price']) for historical in historical_period])
    dates = np.asarray([dateutil.parser.isoparse(historical['begins_at'])for historical in historical_period])

    # format into pandas DataFrame format for ingestion into Backtest
    d = {'Open': open_prices, 'High': highs, 'Low':lows, 'Close': close_prices, 'Datetime': dates}
    d_formated = pd.DataFrame(data=d)
    d_formated.set_index(pd.DatetimeIndex(d['Datetime']), inplace=True)

    bt = Backtest(d_formated, strat,
              cash=cash, commission=0.0,
              exclusive_orders=True, trade_on_close=True)

    # 
    # Outputs below
    
    output = bt.run()
    print('---------------------------------')
    print("Return [%]:  ", output["Return [%]"])
    print('---------------------------------')

 
    optimize_me = bt.optimize(  
                                parabolic_sar_acceleration=list(float_range(0, 0.02, '0.002')),
                                parabolic_sar_maximum=list(float_range(0, 0.5, '0.02')),
                                # sma_shorter=range(10, 30),
                                # sma_longer=range(10, 30),
                                # constraint=lambda p: p.sma_shorter < p.sma_longer
                                )
    # print(optimize_me.to_string())
    print('---------------------------------')
    print("Return [%]:  ", optimize_me["Return [%]"])
    print("what it is  ", optimize_me["_strategy"])
    print('---------------------------------')
  

    # plot it up, plot it up
    if not os.path.exists(f'tests/plots'):
        os.makedirs(f'tests/plots')

    if not os.path.exists(f'tests/plots/{ticker}'):
        os.makedirs(f'tests/plots/{ticker}')
    bt.plot(filename=f"tests/plots/{ticker}/{interval}_{span}.html")


config = get_config_from_args()
StrategyMediator.set_class_vars(config, THE_VERSION_WE_CALL_ONE)
backtest_our_fate(THE_VERSION_WE_CALL_ONE, config)

