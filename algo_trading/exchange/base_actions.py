from abc import abstractmethod

class BaseActions():
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abstractmethod
    def get_account_profile(self, info: str = None):
        pass

    @abstractmethod
    def get_crypto_position(self, info: str = None):
        pass
    
    @abstractmethod
    def get_crypto_order_info(self, id: str):
        pass
    
    @abstractmethod
    def get_crypto_quote(self, symbol: str):
        pass

    @abstractmethod
    def get_crypto_historicals(self, symbol: str, interval: str, span: str, bounds: str):
        pass

    @abstractmethod
    def order_crypto_by_price(self, symbol: str, amountInDollars: float, timeInForce: str):
        pass

    @abstractmethod
    def order_crypto_by_quantity(self, symbol: str, quantity: float, timeInForce: str):
        pass

    @abstractmethod
    def sell_crypto_by_price(self, symbol: str, amountInDollars: float, timeInForce: str):
        pass

    @abstractmethod
    def sell_crypto_by_quantity(self, symbol: str, quantity: float, timeInForce: str):
        pass

    @abstractmethod
    def get_stock_quote(self, symbol: list):
        pass

    @abstractmethod
    def get_stock_historicals(self, symbol: list, interval: str, span: str, bounds: str):
        pass

    @abstractmethod
    def place_order(self, symbol: str, options: dict):
        pass
