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

# imports for strategy, that may be removed when absracted out
from algo_trading.strategies.parabolic_sar import parabolic_sar, ParabolicSAR
from algo_trading.strategies.rsi import rsi, RSI
from algo_trading.strategies.stop_loss import STOP_LOSS
from algo_trading.strategies.sma import SMA_CROSSOVER_TREND, SMA_CROSSOVER_EVENT
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
    config = get_config_from_args()
    print('config:', config)

    p_sar_accel = config['p_sar']['accel']
    p_sar_max = config['p_sar']['max']
    sma_long = config['sma']['long']
    sma_short = config['sma']['short']

    def init(self, position = 0):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low

        self.p_sar = ParabolicSAR(1, self.p_sar_accel, self.p_sar_max)
        self.rsi = RSI(0, 50, 50)
        self.sma = SMA_CROSSOVER_TREND(1, self.sma_long, self.sma_short)
        self.stop_loss = STOP_LOSS(0, -0.1)

        self.indicator_p_sar = self.I(self.p_sar.calcParabolicSAR, high, low)
        self.indicator_rsi = self.I(self.rsi.calcRSI, close)
        self.indicator_sma_long = self.I(self.sma.calcSMA, close, self.sma_long)
        self.indicator_sma_short = self.I(self.sma.calcSMA, close, self.sma_short)

    def next(self):
        current_bid_price = self.data.Close[-1]

        if(len(self.data.Close) > 100):
            p_sar_score = self.p_sar.getScore(current_bid_price, self.data.High, self.data.Low)
            rsi_score = self.rsi.getScore(self.data.Close)
            sma_score = self.sma.getScore(self.data.Close)
            stop_loss_score = self.stop_loss.getScore(self.position.pl_pct)

            scores = np.array([p_sar_score, rsi_score, sma_score])
            average_score = statistics.mean(scores[scores != 0])

            if self.position.size <= 0 and average_score >= 1:
                self.buy()
            elif self.position.size > 0 and (average_score <= -1 or stop_loss_score == -1):
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

    # 
    # Outputs below
    # 
    output = bt.run()
    print('---------------------------------')
    print("Return [%]:  ", output["Return [%]"])
    print('---------------------------------')

    # optimize_me = bt.optimize(  
    #                             p_sar_accel=list(float_range(0, 0.02, '0.002')),
    #                             p_sar_max=list(float_range(0, 0.5, '0.02')),
    #                             # sma_short=range(10, 30),
    #                             # sma_long=range(20, 50),
    #                             # constraint=lambda p: p.sma_short < p.sma_long
    #                             )
    # # print(optimize_me.to_string())
    # print('---------------------------------')
    # print("Return [%]:  ", optimize_me["Return [%]"])
    # print("what it is  ", optimize_me["_strategy"])
    # print('---------------------------------')

    print(' ')
    print('IF THERE IS AN ERROR LIKE <The system cannot find the file specified.> AND YOU ARE USING WSL')
    print('DISREGARD, THIS IS FINE.... I THINK')

    # plot it up, plot it up
    if not os.path.exists(f'tests/plots'):
        os.makedirs(f'tests/plots')

    if not os.path.exists(f'tests/plots/{ticker}'):
        os.makedirs(f'tests/plots/{ticker}')
    bt.plot(filename=f"tests/plots/{ticker}/{interval}_{span}.html")


config = get_config_from_args()

backtest_our_fate(THE_VERSION_WE_CALL_ONE, config)

