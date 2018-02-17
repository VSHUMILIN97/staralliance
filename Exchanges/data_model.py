import time
import logging


class ExchangeModel:
    whole_data = []

    def __init__(self, exchange, pairname, bid, ask):
        self.ask = ask
        self.exchange = exchange
        self.bid = bid
        self.pairname = pairname
        data_merge = {"Exchange": exchange, "PairName": pairname, "Tick": (bid+ask)/2}
        self.whole_data.append(data_merge)

    def pair_swapper(self):
        self.pairname = ""

    def arbitration(self):
        return self.whole_data

    def clear(self):
        self.whole_data.clear()


class EMWrapper(ExchangeModel):

    # data_safe = []

    @staticmethod
    def carrier():
        if ExchangeModel.whole_data:
            return ExchangeModel.whole_data

    # Used to clear the whole list
    @staticmethod
    def cleaar():
        logging.info(ExchangeModel.whole_data)
        ExchangeModel.whole_data.clear()

