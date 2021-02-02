from abc import abstractmethod

class BaseActions():
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abstractmethod
    def get_crypto_quote(self, symbol: str):
        pass

    @abstractmethod
    def get_crypto_historicals(self, symbol: str, interval: str, span: str, bounds: str):
        pass