import time
import logging


class ExchangeModel:
    whole_data = []
    cleared_data = []
    support_data = []

    def __init__(self, exchange, pairname, bid, ask):
        self.ask = ask
        self.exchange = exchange
        self.bid = bid
        self.pairname = pairname
        data_merge = {"Exchange": exchange, "PairName": pairname, "Tick": (bid+ask)/2}
        self.whole_data.append(data_merge)

    def __del__(self):
        None

    def pair_swapper(self):
        print(self.whole_data)

    def arbitration(self):
        return self.whole_data

    def clear(self):
        self.whole_data.clear()

    @staticmethod
    def pair_clearer():
        if ExchangeModel.whole_data:
            for not_safe_pair in ExchangeModel.whole_data:
                ExchangeModel.support_data.append(not_safe_pair.get("PairName"))

            for index, item in enumerate(ExchangeModel.support_data):
                if ExchangeModel.support_data.count(item) >= 2:
                    if item not in ExchangeModel.cleared_data:
                        ExchangeModel.cleared_data.append(item)

            for safe_pair in ExchangeModel.whole_data:
                if safe_pair.get("PairName") not in ExchangeModel.cleared_data:
                    safe_pair.clear()

            while ExchangeModel.whole_data.count({}) != 0:
                ExchangeModel.whole_data.remove({})

            logging.info(ExchangeModel.cleared_data)
            logging.info(len(ExchangeModel.support_data))
            logging.info(len(ExchangeModel.whole_data))
            logging.info(len(ExchangeModel.cleared_data))


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

