import numpy as np
import statistics
import time

from pytz import utc
from apscheduler.schedulers.blocking import BlockingScheduler
from algo_trading.exchange.exchange_context import ExchangeContext
from algo_trading.exchange.robinhood_actions import RobinhoodActions
from algo_trading.enums import Decision
from algo_trading.strategies.strategy_mediator import StrategyMediator
from utils.args import get_config_from_args


class LiveTrading():
    def __init__(self, config, exchange_actions):
        self.symbol = config['symbol']
        self.exchange_actions = exchange_actions
        self.cash = float(0 if self.has_crypto_position() else config['cash'])

        self.interval = config['historicals']['interval']
        self.span = config['historicals']['span']

        self.mediator = StrategyMediator(config)

    def get_historicals(self):
        crypto_historicals = self.exchange_actions.get_crypto_historicals(self.symbol, self.interval, self.span, "24_7")
        print(f"last close price: {crypto_historicals[-1]['close_price']}")
        print(f"last candle begins at: {crypto_historicals[-1]['begins_at']}")
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
    
    def has_crypto_position(self):
        position = self.get_crypto_position()
        return position != None and float(position['quantity_available']) > 0.0

    def get_crypto_quote(self):
        return self.exchange_actions.get_crypto_quote(self.symbol)

    def execute(self):
        order_id = None

        position = self.get_crypto_position()
        current_quote = self.get_crypto_quote()
        
        historicals = self.get_historicals()

        decision = self.mediator.decide(params = {"high": historicals['highs'], "low": historicals['lows'], "close": historicals['close']})

        if not self.has_crypto_position() and descion == Decision.BUY.value:
            # buy
            buying_power = self.get_crypto_buying_power()
            if (self.cash > buying_power):
                raise BaseException(f"Not enough buying power: {buying_power} for given cash amount: {self.cash}")
            else:
                buy_order = self.exchange_actions.order_crypto_by_price(self.symbol, self.cash, 'gtc')
                print(f"BUYING {self.symbol}: {buy_order}")
                order_id = buy_order['id']
                # FOR COINS THAT NEED WHOLE NUMBERS:
                # shares = round(self.cash/float(current_quote['bid_price']), 0)
                # buy_order = self.exchange_actions.order_crypto_by_quantity(self.symbol, shares, 'gtc')
        elif self.has_crypto_position() and descion == Decision.SELL.value:
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

    config = get_config_from_args()

    print('config:', config)
    print('----------')

    live_trading = LiveTrading(config, exchange_actions)
    
    scheduler = BlockingScheduler(timezone=utc)

    if config['historicals']['interval'] == "15second":
        scheduler.add_job(live_trading.execute, 'cron', second="*/15", misfire_grace_time=2)
    elif config['historicals']['interval'] == "5minute":
        scheduler.add_job(live_trading.execute, 'cron', minute="*/5", misfire_grace_time=30)
    elif config['historicals']['interval'] == "hour":
        scheduler.add_job(live_trading.execute, 'cron', hour="*", misfire_grace_time=60)
    else: 
        raise "Invalid interval, please check the config file."
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
