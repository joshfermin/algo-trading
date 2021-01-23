import robin_stocks as r
import pyotp
from bitcoin_price_prediction.settings import RH_PASSWORD, RH_USERNAME, RH_TWO_FACTOR

totp = pyotp.TOTP(RH_TWO_FACTOR).now()
r.login(username=RH_USERNAME, password=RH_PASSWORD, mfa_code=totp)

def show_holdings():
    crypto_positions = r.get_crypto_positions()
    for holding in crypto_positions:
        print(holding)