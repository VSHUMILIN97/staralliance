# https://poloniex.com/public?command=returnTicker
import json
import logging
from django.utils import timezone
import requests
from mongo_db_connection import MongoDBConnection

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


def poloniex_ticker():
    logging.info(u'Poloniex getticker started')
    #
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    test = db.PoloniexTick
    #

    api_request = requests.get("https://poloniex.com/public" + "?command=returnTicker")
    # Формируем JSON массив из данных с API
    json_data = json.loads(api_request.text)
    # Если все ок - парсим
    # Назначаем объект 'result' корневым, для простоты обращения
    js = json_data['BTC_ETH']
    bid, ask = float(js['highestBid']), float(js['lowestAsk'])
    #
    data = {'PairName': 'BTC-ETH', 'Tick': (ask+bid)/2, 'TimeStamp': timezone.now(), 'Mod': False}
    test.insert(data)
    #
    js = json_data['BTC_LTC']
    bid, ask = float(js['highestBid']), float(js['lowestAsk'])
    #
    data = {'PairName': 'BTC-LTC', 'Tick': (ask+bid)/2, 'TimeStamp': timezone.now(), 'Mod': False}
    test.insert(data)
    #
    js = json_data['BTC_DASH']
    bid, ask = float(js['highestBid']), float(js['lowestAsk'])
    #
    data = {'PairName': 'BTC-DASH', 'Tick': (ask + bid) / 2, 'TimeStamp': timezone.now(), 'Mod': False}
    test.insert(data)
    #
    js = json_data['BTC_XRP']
    bid, ask = float(js['highestBid']), float(js['lowestAsk'])
    #
    data = {'PairName': 'BTC-XRP', 'Tick': (ask + bid) / 2, 'TimeStamp': timezone.now(), 'Mod': False}
    test.insert(data)
    logging.info(u'Poloniex getticker ended')
