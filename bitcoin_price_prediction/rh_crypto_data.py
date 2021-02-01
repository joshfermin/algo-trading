"""Script to gather market data from OKCoin Spot Price API."""
import requests
import datetime
import time
from pytz import utc

import bitcoin_price_prediction.robinhood 
import robin_stocks as r

from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from bitcoin_price_prediction.mongo_connect import rh_crypto_collection

collection = rh_crypto_collection()

def tick(symbol):
    aggregate_quote = grab_latest_aggregate_quote(symbol)
    collection.insert_one(aggregate_quote)
    print(aggregate_quote)

def grab_latest_aggregate_quote(symbol):
    quotes = []
    for _ in range(60):
        quotes.append(r.crypto.get_crypto_quote(symbol))
        time.sleep(1)
    
    seq = [quote['bid_price'] for quote in quotes]
    return {
        "high": max(seq),
        "low": min(seq),
        "date": datetime.utcnow().isoformat(),
        "close": quotes[-1]['bid_price'],
        "symbol": symbol
    }

def main():
    """Run tick() at the interval of every ten seconds."""
    scheduler = BlockingScheduler(timezone=utc, job_defaults={'max_instances': 2})
    scheduler.add_job(tick, 'interval', ['BTC'], seconds=60)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == '__main__':
    main()
