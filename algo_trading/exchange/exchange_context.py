from algo_trading.exchange.base_actions import BaseActions

class ExchangeContext():
    """
    The Context defines the interface of interest to clients.
    """

    def __init__(self, strategy: BaseActions) -> None:
        """
        Usually, the Context accepts a strategy through the constructor, but
        also provides a setter to change it at runtime.
        """
        self._strategy = strategy

    @property
    def strategy(self) -> BaseActions:
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It should work
        with all strategies via the Strategy interface.
        """

        return self._strategy

    @strategy.setter
    def strategy(self, strategy: BaseActions) -> None:
        """
        Usually, the Context allows replacing a Strategy object at runtime.
        """

        self._strategy = strategy

    def get_crypto_quote(self, symbol) -> dict:
        """
        The Context delegates some work to the Strategy object instead of
        implementing multiple versions of the algorithm on its own.
        """

        return self._strategy.get_crypto_quote(symbol)

    def get_account_profile(self, info: str = None):
        return self._strategy.get_account_profile(info)

    def get_crypto_historicals(self, symbol: str, interval: str, span: str, bounds: str) -> list:
        return self._strategy.get_crypto_historicals(symbol, interval, span, bounds)
    
    def order_crypto_by_price(self, symbol: str, amountInDollars: float, timeInForce: str) -> dict:
        return self._strategy.order_crypto_by_price(symbol, amountInDollars, timeInForce)

    def order_crypto_by_quantity(self, symbol: str, quantity: float, timeInForce: str) -> dict:
        return self._strategy.order_crypto_by_quantity(symbol, quantity, timeInForce)

    def sell_crypto_by_price(self, symbol: str, amountInDollars: float, timeInForce: str):
        return self._strategy.sell_crypto_by_price(symbol, quantity, timeInForce)

    def sell_crypto_by_quantity(self, symbol: str, quantity: float, timeInForce: str):
       return self._strategy.sell_crypto_by_quantity(symbol, quantity, timeInForce)

