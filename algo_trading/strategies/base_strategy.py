from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    @abstractmethod
    def calculate(self):
        pass

    @abstractmethod
    def indicators(self):
        pass

    @abstractmethod
    def getDecision(self, params):
        pass