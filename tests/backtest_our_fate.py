from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import numpy as np
import pandas as pd
import datetime
import sys, getopt
import statistics
import os
import dateutil.parser

from backtesting.test import GOOG
from algo_trading.enums import Decision

from algo_trading.strategies.strategy_mediator import StrategyMediator
from algo_trading.exchange.exchange_context import ExchangeContext
from algo_trading.exchange.robinhood_actions import RobinhoodActions
from utils.time import handle_time_period
from utils.args import get_config_from_args
from utils.lists import float_range

class THE_VERSION_WE_CALL_ONE(Strategy):
    def init(self, position = 0):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        self.mediator = StrategyMediator(self.config, for_backtesting=True, backtesting_instance=self)
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


def backtest_our_fate(strat, config, should_optimize = False):
    ticker = config['symbol']
    cash = config['cash']
    interval = config['historicals']['interval']
    span = config['historicals']['span']

    start_date = None
    end_date = None
    exchange_actions = ExchangeContext(RobinhoodActions())
    crypto_historicals = exchange_actions.get_crypto_historicals(ticker, interval=interval, span=span, bounds="24_7")

    # start_date = datetime.datetime(2021, 1, 2)
    # end_date = datetime.datetime(2021, 2, 6)

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

    # Outputs below
    output = bt.run()
    print('---------------------------------')
    print("Return [%]:  ", output["Return [%]"])
    print('---------------------------------')
    
    if (should_optimize):
        # TODO: make this dynamic, let strategy mediator return a **kwargs of params
        optimize_me = bt.optimize(  
            # parabolic_sar_acceleration=list(float_range(0, 0.02, '0.002')),
            # parabolic_sar_maximum=list(float_range(0, 0.5, '0.02')),
            sma_shorter=range(10, 30),
            sma_longer=range(20, 50),
            # rsi_high=range(1,100),
            # rsi_low=range(1,100),
            constraint=lambda p: p.sma_shorter < p.sma_longer,
            maximize="Return [%]"
        )

        print('---------------------------------')
        print("Return [%]:  ", optimize_me["Return [%]"])
        print("what it is  ", optimize_me["_strategy"])
        print('---------------------------------')

    print(' ')
    print('IF THERE IS AN ERROR LIKE <The system cannot find the file specified.> AND YOU ARE USING WSL')
    print('DISREGARD, THIS IS FINE.... I THINK')

    plot_backtest_results(bt, ticker, interval, span)

def plot_backtest_results(bt, ticker, interval, span):
    if not os.path.exists(f'tests/plots'):
        os.makedirs(f'tests/plots')

    if not os.path.exists(f'tests/plots/{ticker}'):
        os.makedirs(f'tests/plots/{ticker}')
    
    bt.plot(filename=f"tests/plots/{ticker}/{interval}_{span}.html")

def main():
    # TODO: do we want to take inputs from user here? i.e. choose config, choose start/end etc
    # TODO: or maybe even nuttier, just create a UI WRAPPER for this
    config = get_config_from_args()
    THE_VERSION_WE_CALL_ONE.config = config
    StrategyMediator.set_class_vars(config, THE_VERSION_WE_CALL_ONE)
    backtest_our_fate(THE_VERSION_WE_CALL_ONE, config)

if __name__ == '__main__':
    main()
