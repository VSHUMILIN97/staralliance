import time
import logging


# Class wrapper for DATA from Exchanges
class ExchangeModel:
    # Supported arrays.
    whole_data = []
    cleared_data = []
    support_data = []

    # Class initialise
    def __init__(self, exchange, pairname, bid, ask):
        self.ask = ask
        self.exchange = exchange
        self.bid = bid
        self.pairname = pairname
        data_merge = {"Exchange": exchange, "PairName": pairname, "Tick": (bid+ask)/2}
        self.whole_data.append(data_merge)

    # Garbage collector
    def __del__(self):
        None

    def clear(self):
        self.whole_data.clear()

    """
    This method crop full data to cleared small pieces, step by step:
    1) PairName that supported by more than two Exchanges appended to support_data, creating cleared pair_list->
    2) Appending data from full DATA list to cleared_data using cleared pair_list ->
    3) Then cleaning the whole data, if it's not like clear_data.
    IMPORTANT. WE DO NOT SEND CLEARED DATA, BECAUSE IT'S NOT FULL AND DOES NOT CONTAIN ALL THE INFORMATION
    """
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
