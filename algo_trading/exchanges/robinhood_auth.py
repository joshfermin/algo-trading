import robin_stocks as r
import pyotp
from algo_trading.settings import RH_PASSWORD, RH_USERNAME, RH_TWO_FACTOR

r.login(username=RH_USERNAME, password=RH_PASSWORD, mfa_code=pyotp.TOTP(RH_TWO_FACTOR).now())