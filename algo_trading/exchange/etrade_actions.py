import pyetrade
from algo_trading.settings import ETRADE_KEY, ETRADE_SECRET
from algo_trading.exchange.base_actions import BaseActions

class EtradeActions(BaseActions):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """
    def __init__(self):
        oauth = pyetrade.ETradeOAuth(consumer_key, consumer_secret)
        verifier_code = input("Enter E-Trade verification code: ")
        tokens = oauth.get_access_token(verifier_code)

        self.market = pyetrade.ETradeMarket(
            consumer_key,
            consumer_secret,
            tokens['oauth_token'],
            tokens['oauth_token_secret'],
            dev=True
        )

        self.orders = pyetrade.ETradeOrder(
            consumer_key,
            consumer_secret,
            tokens['oauth_token'],
            tokens['oauth_token_secret'],
            dev=True
        )

        self.accounts = pyetrade.ETradeAccounts(
            consumer_key,
            consumer_secret,
            tokens['oauth_token'],
            tokens['oauth_token_secret'],
            dev=True
        )


    def get_crypto_quote(self, symbol: str) -> dict:
        raise NotImplementedError

    def order_crypto_by_price(self, symbol: str, amountInDollars: float, timeInForce: str):
         raise NotImplementedError

    def get_crypto_historicals(self, symbol: str, interval: str, span: str, bounds: str) -> list:
        raise NotImplementedError

    def get_stock_quote(self, symbol: list(str)) -> dict:
        self.market.get_quote(symbol, resp_format='json')

    def get_stock_historicals(self, options: dict) -> list:
        raise NotImplementedError

    def place_order(self, symbol, options: dict) -> dict:
        # self.orders.place_equity_order()
        raise NotImplementedError