import robin_stocks as r
import pyotp
from algo_trading.settings import RH_PASSWORD, RH_USERNAME, RH_TWO_FACTOR
from algo_trading.exchange.base_actions import BaseActions

class RobinhoodActions(BaseActions):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """
    def __init__(self):
        r.login(username=RH_USERNAME, password=RH_PASSWORD, mfa_code=pyotp.TOTP(RH_TWO_FACTOR).now())

    def get_crypto_quote(self, symbol: str) -> dict:
        return r.crypto.get_crypto_quote(symbol)

    def order_crypto_by_price(self, symbol: str, amountInDollars: float, timeInForce: str) -> dict:
        return r.orders.order_buy_crypto_by_price(symbol, amountInDollars, timeInForce)

    def order_crypto_by_quantity(self, symbol: str, quantity: float, timeInForce: str) -> dict:
        return r.orders.order_buy_crypto_by_quantity(symbol, quantity, timeInForce)

    def get_crypto_historicals(self, symbol: str, interval: str, span: str, bounds: str) -> list:
        return r.get_crypto_historicals(symbol, interval=interval, span=span, bounds=bounds)
    
    def get_stock_quote(self, symbol: str) -> dict:
        return r.stocks.get_stock_quote_by_symbol(symbol)

    def get_stock_historicals(self, symbol: str, interval: str, span: str, bounds: str):
        return r.stocks.get_stock_historicals([symbol], interval=interval, span=span, bounds=bounds, info=None)

    def order(self, symbol: str, options: dict) -> dict:
        """
        A generic order function.

        Parameters:	
        symbol (str) – The stock ticker of the stock to sell.
        quantity (int) – The number of stocks to sell.
        side (str) – Either ‘buy’ or ‘sell’
        limitPrice (float) – The price to trigger the market order.
        stopPrice (float) – The price to trigger the limit or market order.
        timeInForce (str) – Changes how long the order will be in effect for. ‘gtc’ = good until cancelled. ‘gfd’ = good for the day.
        extendedHours (Optional[str]) – Premium users only. Allows trading during extended hours. Should be true or false.
        jsonify (Optional[str]) – If set to False, function will return the request object which contains status code and headers.
        Returns:	
        Dictionary that contains information regarding the purchase or selling of stocks, such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), the price, and the quantity.
        """
        
        return r.orders.order(
            symbol, 
            options['quantity'], 
            options['side'], 
            limitPrice=options.get('limitPrice'), 
            stopPrice=options.get('stopPrice'), 
            timeInForce=options.get('timeInForce'), 
            extendedHours=options.get('extendedHours'), 
            jsonify=True
        )