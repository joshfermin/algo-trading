from algo_trading.historicals.base_historicals import BaseHistoricals

class HistoricalsContext(BaseHistoricals):
    def __init__(self, strategy: BaseHistoricals) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> BaseHistoricals:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: BaseHistoricals) -> None:
        self._strategy = strategy

    def get_crypto_historicals(self, symbol, interval, span) -> dict:
        return self._strategy.get_crypto_historicals(symbol, interval, span)