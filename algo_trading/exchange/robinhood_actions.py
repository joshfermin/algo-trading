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

    def get_crypto_quote(self, symbol: str = 'ETH') -> dict:
        return r.crypto.get_crypto_quote(symbol)

    def get_crypto_historicals(self, symbol: str, interval: str, span: str, bounds: str) -> list:
        return r.get_crypto_historicals(symbol, interval=interval, span=span, bounds=bounds)