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
from algo_trading.historicals.historicals_context import HistoricalsContext
from algo_trading.historicals.mongodb_historicals import MongoDbHistoricals
from algo_trading.historicals.robinhood_historicals import RobinhoodHistoricals
from utils.time import handle_time_period
from utils.args import get_config_from_args
from utils.lists import float_range

class THE_VERSION_WE_CALL_ONE(Strategy):
    def init(self, position = 0):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        volume = self.data.Volume
        self.mediator = StrategyMediator(self.config, for_backtesting=True, backtesting_instance=self)
        self.mediator.setup_indicators(self, high, low, close, volume)

    def next(self):
        current_bid_price = self.data.Close[-1]

        decision = self.mediator.decide({"high": self.data.High, "low": self.data.Low, "close": self.data.Close, "volume": self.data.Volume}, self.position.size > 0)
        
        if decision == Decision.BUY:
            self.buy()
        elif decision == Decision.SELL:
            self.position.close()

        relative_position = self.position.size if self.position.size >= 0 else 0


def backtest_our_fate(strat, config, historicals, should_optimize = False):
    ticker = config['symbol']
    cash = config['cash']
    interval = config['historicals']['interval']
    span = config['historicals']['span']

    bt = Backtest(historicals, strat,
              cash=cash, commission=0.0,
              exclusive_orders=True, trade_on_close=True)

    # Outputs below
    output = bt.run()
    print('---------------------------------')
    print("Return [%]:  ", output["Return [%]"])
    print('---------------------------------')

    # print('---------------------------------')
    # print("Return [%] by holding:  ", (float(crypto_historicals[-1]['close_price']) - float(crypto_historicals[0]['close_price'])) / float(crypto_historicals[0]['close_price']) * 100  )
    # print('---------------------------------')
    
    if (should_optimize):
        # TODO: make this dynamic, let strategy mediator return a **kwargs of params
        optimize_me = bt.optimize(
            parabolic_sar_acceleration=list(float_range(0, 0.02, '0.002')),
            parabolic_sar_maximum=list(float_range(0, 0.5, '0.02')),
            # ema_period=range(9, 50),
            # sma_shorter=range(5, 30),
            # sma_longer=range(15, 60),
            # rsi_high=range(1,100),
            # rsi_low=range(1,100),
            # constraint=lambda p: p.rsi_low < p.rsi_high,
            maximize="Return [%]"
        )

        print('---------------------------------')
        print("Return [%]:  ", optimize_me["Return [%]"])
        print("what it is  ", optimize_me["_strategy"])
        print('---------------------------------')

    plot_backtest_results(bt, ticker, interval, span)

def plot_backtest_results(bt, ticker, interval, span):
    print(interval, span)
    if not os.path.exists(f'tests/plots'):
        os.makedirs(f'tests/plots')

    if not os.path.exists(f'tests/plots/{ticker}'):
        os.makedirs(f'tests/plots/{ticker}')
    
    bt.plot(filename=f"tests/plots/{ticker}/{interval}_{span}.html")

def main():
    # TODO: do we want to take inputs from user here? i.e. choose config, choose start/end etc
    # TODO: or maybe even nuttier, just create a UI WRAPPER for this
    config = get_config_from_args()

    ticker = config['symbol']
    cash = config['cash']
    interval = config['historicals']['interval']
    span = config['historicals']['span']

    THE_VERSION_WE_CALL_ONE.config = config
    StrategyMediator.set_class_vars_for_optimize(config, THE_VERSION_WE_CALL_ONE)
    
    historical_context = HistoricalsContext(MongoDbHistoricals())
    historicals = historical_context.normalize_historicals_for_backtest(ticker, interval, span)

    backtest_our_fate(THE_VERSION_WE_CALL_ONE, config, historicals, False)

if __name__ == '__main__':
    main()
