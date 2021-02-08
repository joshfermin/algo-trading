import numpy as np
import statistics

from pytz import utc
from apscheduler.schedulers.blocking import BlockingScheduler
from algo_trading.exchange.exchange_context import ExchangeContext
from algo_trading.exchange.robinhood_actions import RobinhoodActions
from algo_trading.strategies.parabolic_sar import ParabolicSAR
from algo_trading.strategies.sma import SMA_CROSSOVER_TREND


class LiveTrading():
    p_sar_accel = 0.015
    p_sar_max = 0.06
    sma_long = 46
    sma_short = 21

    def __init__(self, symbol, exchange_actions, sell_amount=None):
        self.symbol = symbol
        self.exchange_actions = exchange_actions
        self.sell_amount = sell_amount
        self.p_sar = ParabolicSAR(1, self.p_sar_accel, self.p_sar_max)
        self.sma = SMA_CROSSOVER_TREND(1, self.sma_long, self.sma_short)

    def get_historicals(self):
        crypto_historicals = self.exchange_actions.get_crypto_historicals(self.symbol, "hour", "3month", "24_7")
        print(crypto_historicals[-1])
        close_prices = np.asarray([float(historical['close_price']) for historical in crypto_historicals])
        open_prices = np.asarray([float(historical['open_price']) for historical in crypto_historicals])
        highs = np.asarray([float(historical['high_price']) for historical in crypto_historicals])
        lows = np.asarray([float(historical['low_price']) for historical in crypto_historicals])
        return {
            'close': close_prices,
            'open': open_prices,
            'highs': highs,
            'lows': lows
        }

    def get_crypto_buying_power(self):
        return self.exchange_actions.get_account_profile('crypto_buying_power')
    
    def get_crypto_position(self):
        return next((x for x in self.exchange_actions.get_crypto_positions() if x['currency']['code'] == self.symbol), None)

    def get_crypto_quote(self):
        return self.exchange_actions.get_crypto_quote(self.symbol)

    def execute(self):
        position = self.get_crypto_position()
        current_quote = self.get_crypto_quote()
        
        historicals = self.get_historicals()

        p_sar_score = self.p_sar.getScore(historicals['close'][-1], historicals['highs'], historicals['lows'])
        sma_score = self.sma.getScore(historicals['close'])
        
        scores = np.array([p_sar_score, sma_score])
        average_score = statistics.mean(scores[scores != 0])

        if (position == None or float(position['quantity_available']) == 0.0 ) and average_score >= 1:
            # buy
            buying_power = self.get_crypto_buying_power()
            print(f"BUYING ETH: {buying_power}")
        elif float(position['quantity_available']) > 0.0 and average_score == -1:
            # sell
            position_quantity = self.get_crypto_position()['quantity_available']
            print(f"SELLING ETH: {position_quantity}")


def main():
    exchange_actions = ExchangeContext(RobinhoodActions())
    live_trading = LiveTrading('ETH', exchange_actions)
    
    scheduler = BlockingScheduler(timezone=utc)
    scheduler.add_job(live_trading.execute, 'cron', hour="*")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
