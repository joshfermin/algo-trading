import importlib
import numpy as np
import statistics

from utils.args import get_config_from_args

class StrategyMediator():
    STRATEGY_MODULE_NAME = "algo_trading.strategies"
    WEIGHT = 1

    def __init__(self, config, for_backtesting = False, backtesting_instance = None):
        if not "strategies" in config:
            raise Exception("`strategies` key required in config.")

        self.config = config
        self.strategies = []
        for strategy in config['strategies']:
            strategy_class = getattr(importlib.import_module(f"algo_trading.strategies.{strategy['name']}"), strategy['name'])
            if for_backtesting:
                strategy_params = {}
                for param in strategy['params']:
                    strategy_params[param] = getattr(backtesting_instance, f"{strategy['name']}_{param}")
                self.strategies.append(strategy_class(**strategy_params))
            if not for_backtesting:
                strategy_instance = strategy_class(**strategy['params'])
                self.strategies.append(strategy_instance)

    def decide(self, params = {"high": None, "low": None, "close": None}):
        decision = None
        scores = []
        
        for strategy in self.strategies:
            scores.append(float(strategy.getDecision(params).value))

        return statistics.mean(scores)
              
    def setup_indicators(self, backtesting_class_context, highs, lows, closes):
        for strategy in self.strategies:
            indicators = strategy.indicators()
            calculate_params = strategy.calculate.__code__.co_varnames
            
            for indicator in indicators:
                params = {} 
                if 'params' in indicator: params = indicator['params']
                if 'close_prices' in calculate_params: params['close_prices'] = closes
                if 'highs' in calculate_params: params['highs'] = highs
                if 'lows' in calculate_params: params['lows'] = lows
                setattr(backtesting_class_context, indicator['name'], backtesting_class_context.I(strategy.calculate, **params, name = indicator['name']))
    
    @staticmethod
    def set_class_vars(config, klass):
        for strategy in config['strategies']:
            for key, value in strategy['params'].items():
                setattr(klass, f"{strategy['name']}_{key}", value)
