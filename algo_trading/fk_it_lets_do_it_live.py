import numpy as np
import statistics
import time

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

    def __init__(self, symbol, exchange_actions, cash=None):
        self.symbol = symbol
        self.exchange_actions = exchange_actions
        self.cash = cash
        self.p_sar = ParabolicSAR(1, self.p_sar_accel, self.p_sar_max)
        self.sma = SMA_CROSSOVER_TREND(1, self.sma_long, self.sma_short)

    def get_historicals(self):
        crypto_historicals = self.exchange_actions.get_crypto_historicals(self.symbol, "15second", "hour", "24_7")
        print(f"last close price: {crypto_historicals[-1]['close_price']}")
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
        return float(self.exchange_actions.get_account_profile('crypto_buying_power'))
    
    def get_crypto_position(self):
        return next((x for x in self.exchange_actions.get_crypto_positions() if x['currency']['code'] == self.symbol), None)

    def get_crypto_quote(self):
        return self.exchange_actions.get_crypto_quote(self.symbol)

    def execute(self):
        order_id = None

        position = self.get_crypto_position()
        current_quote = self.get_crypto_quote()
        
        historicals = self.get_historicals()

        p_sar_score = self.p_sar.getScore(historicals['close'][-1], historicals['highs'], historicals['lows'])
        sma_score = self.sma.getScore(historicals['close'])
        
        scores = np.array([p_sar_score, sma_score])
        average_score = statistics.mean(scores[scores != 0])

        if (position == None or float(position['quantity_available']) == 0.0) and average_score >= 1:
            # buy
            buying_power = self.get_crypto_buying_power()
            if (self.cash > buying_power):
                raise BaseException(f"Not enough buying power: {buying_power} for given cash amount: {self.cash}")
            else:
                buy_order = self.exchange_actions.order_crypto_by_price(self.symbol, self.cash, 'gtc')
                order_id = buy_order['id']
                # FOR COINS THAT NEED WHOLE NUMBERS:
                # shares = round(self.cash/float(current_quote['bid_price']), 0)
                # buy_order = self.exchange_actions.order_crypto_by_quantity(self.symbol, shares, 'gtc')
                print(f"BUYING {self.symbol}: {buy_order}")
        elif position != None and float(position['quantity_available']) > 0.0 and average_score == -1:
            # sell
            position_quantity = float(self.get_crypto_position()['quantity_available'])
            sell_order = self.exchange_actions.sell_crypto_by_quantity(self.symbol, position_quantity, "gtc")
            print(f"SELLING {self.symbol}: {sell_order}")
            order_id = sell_order['id']

        if (order_id != None):
            order = self.exchange_actions.get_crypto_order_info(order_id)
            while order['cancel_url'] != None:
                order = self.exchange_actions.get_crypto_order_info(order_id)
                time.sleep(5)
            amount_usd = float(order['rounded_executed_notional'])
            order_side = order['side']
            if order_side == 'sell':
                self.cash += amount_usd
            elif order_side == 'buy':
                self.cash -= amount_usd
            print("----")
            print(f"cash: {self.cash}, side: {order_side}, usd_amount: {amount_usd}")

def main():
    exchange_actions = ExchangeContext(RobinhoodActions())
    live_trading = LiveTrading('DOGE', exchange_actions, 1.00)
    
    scheduler = BlockingScheduler(timezone=utc)
    scheduler.add_job(live_trading.execute, 'cron', second="*/15")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
