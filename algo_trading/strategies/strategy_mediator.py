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

        self.config = config
        self.strategies = []
        for strategy in config['strategies']:
            strategy_class = getattr(importlib.import_module(f"algo_trading.strategies.{strategy['name']}"), strategy['name'])
            strategy_instance = strategy_class(**strategy['params'])
            self.strategies.append(strategy_instance)

    def decide(self, params = {"high": None, "low": None, "close": None}):
        decision = None
        scores = []
        
        for strategy in self.strategies:
            scores.append(float(strategy.getDecision(params).value))

        return statistics.mean(scores)

    def set_class_vars(self, klass):
        for strategy in self.config['strategies']:
            for key, value in strategy['params'].items():
                setattr(klass, key, value)
              
    def setup_indicators(self, backtesting_class_context, highs, lows, closes):
        for strategy in self.strategies:
            indicators = strategy.indicators()

            # all the args from calculate
            # match high low or close and params from indicator -> dictionary -> **kwargs
            calculate_params = strategy.calculate.__code__.co_varnames
            
            for indicator in indicators:
                params = {} 
                if 'params' in indicator: params = indicator['params']
                #  for key, value in params.items():
                #         setattr(backtesting_class_context.__class__, indicator['name'], value)
                #         params[key] = getattr(backtesting_class_context.__class__, indicator['name'])
                #         print(params[key])
                if 'close_prices' in calculate_params: params['close_prices'] = closes
                if 'highs' in calculate_params: params['highs'] = highs
                if 'lows' in calculate_params: params['lows'] = lows
                setattr(backtesting_class_context, indicator['name'], backtesting_class_context.I(strategy.calculate, **params, name = indicator['name']))
