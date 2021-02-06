"""Script to gather market data from OKCoin Spot Price API."""
import requests
import dateutil.parser
from pytz import utc
from datetime import datetime
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
from algo_trading.mongo_connect import historical_data_collection
from pymongo import errors

def record_data(symbol, instrument_id, granularity_in_seconds, granularity_name):
    collection = historical_data_collection(symbol, granularity_name)
    """Gather market data from OKCoin Spot Price API and insert them into a
       MongoDB collection."""

    candles = requests.get(f'https://www.okcoin.com/api/spot/v3/instruments/{instrument_id}/candles?granularity={granularity_in_seconds}').json()
    documents = []
    for candle in candles:
        documents.append({
            "date": dateutil.parser.isoparse(candle[0]),
            "open": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4]),
            "volume": float(candle[5]),
        })
    try:
        # inserts new documents even on error
        collection.insert_many(documents)
    except errors.BulkWriteError as e:
        panic_list = list(filter(lambda x: x['code'] != 11000, e.details['writeErrors']))
        if len(panic_list) > 0:
            print(f"these are not duplicate errors {panic_list}")

def main():
    """Run tick() at the interval of every ten seconds."""
    scheduler = BlockingScheduler(timezone=utc)
    scheduler.add_job(record_data, 'cron', ['ETH', 'ETH-USD', 86400, 'day'], day="*")
    scheduler.add_job(record_data, 'cron', ['ETH', 'ETH-USD', 3600, 'hour'], hour="*")
    scheduler.add_job(record_data, 'cron', ['ETH', 'ETH-USD', 300, 'five_minutes'], minute="*/5")
    scheduler.add_job(record_data, 'cron', ['ETH', 'ETH-USD', 60, 'one_minute'], minute="*")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
