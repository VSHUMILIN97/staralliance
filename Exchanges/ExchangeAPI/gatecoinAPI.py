# https://api.gatecoin.com/Public/LiveTickers
import json
import logging
from django.utils import timezone
import requests
from Exchanges.data_model import ExchangeModel
from mongo_db_connection import MongoDBConnection

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


# Боевая задачка - написать неунифицированные парсилки пар, чтобы все совпадало. Без хардкода.
pairlist = ['ETHBTC', '1STBTC', 'LTCBTC', 'LTCETH']
coins = ['ETH', 'BTC', 'LTC', 'DASH', 'XRP', '1ST', '123', 'POE', 'MANA', 'LSK', 'EVX', 'ICN', 'QAX', 'XVG', 'SNM',
         'IOTA', 'NEO', 'MTL', 'YOYO', 'BNB', 'BCC', 'ZEC', 'BTG', 'REQ']


def pair_fix(pair_string):
    for i in range(0, len(coins)):
        if str(pair_string).startswith(coins[i]) is True:
            test = str(pair_string).replace(coins[i], coins[i] + '-')
            test.split('-')
            pair_string = test[1] + '-' + test[0]
            return pair_string
        else:
            return pair_string

def gatecoin_ticker():
    logging.info(u'Gatecoin collection of data in parse')

    try:
        b = MongoDBConnection().start_db()
        db = b.PiedPiperStock
        gcstock = db.GatecoinTick
        api_request = requests.get("https://api.gatecoin.com/Public/LiveTickers")
        #
        logging.info('Gatecoin API returned - ' + str(api_request.status_code))
        if api_request.status_code == 200:
            json_data = json.loads(api_request.text)
            result = json_data['tickers']
            for item in result:
                ExchangeModel("Gatecoin", pair_fix(item['currencyPair']), float(item['bid']), float(item['ask']))
                if item['currencyPair'] in pairlist:
                    market, bid, ask = str(item['currencyPair']), float(item['bid']), float(item['ask'])
                    data = {'PairName': pair_fix(market), 'Tick': (bid + ask)/2,
                            'TimeStamp': timezone.now(), 'Mod': False}
                    gcstock.insert(data)
                else:
                    continue
        MongoDBConnection().stop_connect()
    except():
        logging.error(r'Gatecoin ticker mistake')