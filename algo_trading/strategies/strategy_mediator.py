import importlib
import numpy as np
import statistics

from utils.args import get_config_from_args

class StrategyMediator():
    STRATEGY_MODULE_NAME = "algo_trading.strategies"
    WEIGHT = 1

    def __init__(self, config):
        if not "strategies" in config:
            raise Exception("`strategies` key required in config.")
        
        self.strategies = []
        for strategy in config['strategies']:
            strategy_class = getattr(importlib.import_module(f"algo_trading.strategies.{strategy['name']}"), strategy['name'])
            strategy_instance = strategy_class(strategy['params'])
            self.strategies.append(strategy_instance)

    def decide(self, params = {"high": None, "low": None, "close": None}):
        decision = None
        scores = []
        
        for strategy in self.strategies:
            scores.append(float(strategy.getDecision(params).value))

        return statistics.mean(scores)


# config = get_config_from_args()
# StrategyMediator(config)
