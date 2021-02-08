class STOP_LOSS:
    def __init__(self, weight, stop_percent):
        self.weight = weight
        self.stop_percent = stop_percent

    def getScore(self, profit_loss_percent):
        if profit_loss_percent <= self.stop_percent:
            # SELL
            return -1 * self.weight

