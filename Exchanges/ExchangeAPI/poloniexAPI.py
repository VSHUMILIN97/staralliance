# https://poloniex.com/public?command=returnTicker
import json
import logging
from django.utils import timezone
import requests
from mongo_db_connection import MongoDBConnection

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

pairlist = ['BTC_ETH', 'BTC_LTC', 'BTC_DASH', 'BTC_XRP']


def pair_fix(pair_string):
    if str(pair_string).split('_')[0] == 'BTC':
        a = str(pair_string).split('_')[0]
        b = str(pair_string).split('_')[1]
        c = b + "-" + a
        return c
    else:
        return str(pair_string).replace('_', '-')


def poloniex_ticker():
    logging.info(u'Poloniex getticker started')
    #
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    test = db.PoloniexTick
    #

    api_request = requests.get("https://poloniex.com/public" + "?command=returnTicker")
    #
    logging.info('Poloniex API returned - ' + str(api_request.status_code))
    if api_request.status_code == 200:
        json_data = json.loads(api_request.text)
        for item in json_data:
            if item in pairlist:
                bid, ask = float(json_data[item]['highestBid']), float(json_data[item]['lowestAsk'])
                data = {'PairName': pair_fix(item), 'Tick': (ask + bid) / 2, 'TimeStamp': timezone.now(), 'Mod': False}
                test.insert(data)
    logging.info(u'Poloniex getticker ended')
