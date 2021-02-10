from enum import Enum

class Decision(Enum):
    BUY = 1
    SELL = -1
    NOOP = 0