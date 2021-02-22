from enum import Enum

class Decision(Enum):
    BUY = 1.0
    SELL = -1.0
    NOOP = 0.0

class GatedDecision(Enum):
    CONTINUE_TRADING = False
    STOP_TRADING = True
