import dateutil.parser

from algo_trading.exchange.exchange_context import ExchangeContext
from algo_trading.exchange.robinhood_actions import RobinhoodActions
from algo_trading.historicals.base_historicals import BaseHistoricals

class RobinhoodHistoricals(BaseHistoricals):
    def get_crypto_historicals(self, symbol, interval, span,):
            # start_date = datetime.datetime(2021, 1, 2)
        # end_date = datetime.datetime(2021, 2, 6)
        exchange_actions = ExchangeContext(RobinhoodActions())
        rh_historicals = exchange_actions.get_crypto_historicals(symbol, interval=interval, span=span, bounds="24_7")
        
        historicals = []
        for historical in rh_historicals:
            historicals.append(
                {
                    'close_price': float(historical['close_price']),
                    'open_price': float(historical['open_price']),
                    'high_price': float(historical['high_price']),
                    'low_price': float(historical['low_price']),
                    'volume': float(historical['volume']),
                    'date': dateutil.parser.isoparse(historical['begins_at'])
                }
            )
        
        return historicals

