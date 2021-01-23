"""Script to gather market data from OKCoin Spot Price API."""
import requests
import dateutil.parser
from pytz import utc
from datetime import datetime
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
from bitcoin_price_prediction.mongo_connect import historical_data_collection

collection = historical_data_collection()


def tick():
    """Gather market data from OKCoin Spot Price API and insert them into a
       MongoDB collection."""
    ticker = requests.get('https://www.okcoin.com/api/spot/v3/instruments/BTC-USD/ticker').json()
    depth = requests.get('https://www.okcoin.com/api/spot/v3/instruments/BTC-USD/book?size=60').json()
    date = dateutil.parser.isoparse(ticker['timestamp'])
    price = float(ticker['last'])
    v_bid = sum([float(bid[1]) for bid in depth['bids']])
    v_ask = sum([float(ask[1]) for ask in depth['asks']])
    collection.insert_one({'date': date, 'price': price, 'v_bid': v_bid, 'v_ask': v_ask})
    print(date, price, v_bid, v_ask)

def main():
    """Run tick() at the interval of every ten seconds."""
    scheduler = BlockingScheduler(timezone=utc)
    scheduler.add_job(tick, 'interval', seconds=10)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
