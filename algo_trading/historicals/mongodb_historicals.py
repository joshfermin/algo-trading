from algo_trading.mongo_connect import historical_data_collection
from algo_trading.historicals.base_historicals import BaseHistoricals

class MongoDbHistoricals(BaseHistoricals):
    def get_crypto_historicals(self, symbol, interval, span,):
        collection = historical_data_collection(symbol, interval)
        historicals = []
        
        num_points = 777600
        for doc in collection.find().sort('_id', -1).limit(num_points):
            historicals.append(
                {
                    "date": doc["date"],
                    "open_price": doc["open"],
                    "high_price": doc["high"],
                    "low_price": doc["low"],
                    "close_price": doc["close"],
                    "volume": doc["volume"]
                }
            )
        return historicals