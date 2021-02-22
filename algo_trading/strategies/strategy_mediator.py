import importlib
import numpy as np
import statistics

from algo_trading.enums import Decision
from utils.args import get_config_from_args

class StrategyMediator():
    STRATEGY_MODULE_NAME = "algo_trading.strategies"
    WEIGHT = 1

    def __init__(self, config, for_backtesting = False, backtesting_instance = None):
        if not "strategies" in config:
            raise Exception("`strategies` key required in config.")

        self.config = config
        self.for_backtesting = for_backtesting
        self.backtesting_instance = backtesting_instance
        self.strategies = self.__instantiate_strategy_classes()


    def decide(self, params = {"high": None, "low": None, "close": None}, has_position = None):
        decision = None
        scores = []
        gated_decisions = []
        
        for strategy in self.strategies:
            decision = strategy.getDecision(params).value
            if isinstance(decision, float):
                scores.append(decision)
            if isinstance(decision, bool):
                gated_decisions.append(decision)
            
        # if any gated decision says to stop trading, send back noop if no current position
        if not has_position and any(gated_decisions):
            return Decision.NOOP

        computed_strategy_decision = {
            1: Decision.BUY,
            -1: Decision.SELL
        }.get(statistics.mean(scores), Decision.NOOP)

        if has_position and computed_strategy_decision == Decision.SELL:
            return Decision.SELL
        if not has_position and computed_strategy_decision == Decision.BUY:
            return Decision.BUY
        return Decision.NOOP
              
    def setup_indicators(self, backtesting_class_context, highs, lows, closes, volumes):
        for strategy in self.strategies:
            indicators = strategy.indicators()
            calculate_params = strategy.calculate.__code__.co_varnames
            
            for indicator in indicators:
                params = {} 
                if 'params' in indicator: params = indicator['params']
                if 'close_prices' in calculate_params: params['close_prices'] = closes
                if 'volumes' in calculate_params: params['volumes'] = volumes
                if 'highs' in calculate_params: params['highs'] = highs
                if 'lows' in calculate_params: params['lows'] = lows
                setattr(backtesting_class_context, indicator['name'], backtesting_class_context.I(strategy.calculate, **params, name = indicator['name']))
    
    @staticmethod
    def set_class_vars_for_optimize(config, klass):
        for strategy in config['strategies']:
            if "params" in strategy:
                for key, value in strategy['params'].items():
                    setattr(klass, f"{strategy['name']}_{key}", value)

    def __instantiate_strategy_classes(self):
        strategies = []
        try:
            for strategy in self.config['strategies']:
                strategy_klass = getattr(importlib.import_module(f"algo_trading.strategies.{strategy['name']}"), strategy['name'])
                if not 'params' in strategy:
                    strategies.append(strategy_klass())
                else:
                    if self.for_backtesting:
                        strategy_params = {}
                        for param in strategy['params']:
                            strategy_params[param] = getattr(self.backtesting_instance, f"{strategy['name']}_{param}")
                        strategies.append(strategy_klass(**strategy_params))
                    elif not self.for_backtesting:
                        strategies.append(strategy_klass(**strategy['params']))
                       
            return strategies
        except TypeError as err:
            raise f"Please check your config is set up correctly for: ${strategy_klass.__name__}, Error: {err}"
    
