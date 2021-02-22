from enum import Enum

class Decision(Enum):
    BUY = 1.0
    SELL = -1.0
    NOOP = 0.0

class GatedDecision(Enum):
    CAN_HOLD_LONG_POSITION = False
    CAN_HOLD_SHORT_POSITION = True
