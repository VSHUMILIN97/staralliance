# https://api.kucoin.com/v1/open/tick
import json
import logging
from django.utils import timezone
import requests
from Exchanges.data_model import ExchangeModel
from mongo_db_connection import MongoDBConnection


def pair_fix(pair_string):
    fixer = pair_string.split('-')
    pair_string = fixer[1] + '-' + fixer[0]
    return pair_string


def kucoin_ticker():
    # Данные собираются для каждой валютной пары из списка pairlist
    logging.info(u'Bleutrade getticker started')
    try:
        #
        b = MongoDBConnection().start_db()
        db = b.PiedPiperStock
        test = db.KucoinTick
        #
        info_request = requests.get("https://api.kucoin.com/v1/open/tick")
        info_data = json.loads(info_request.text)
        if info_data['code'] == 'OK':
            data = info_data['data']
            for item in data:
                try:
                    ExchangeModel('Kucoin', pair_fix(item['symbol']), float(item['buy']), float(item['sell']))
                except KeyError:
                    continue
                try:
                    bid, ask = float(item['buy']), float(item['sell'])
                except KeyError:
                    continue
                #
                data = {'PairName': pair_fix(item['symbol']), 'Tick': (ask+bid)/2,
                        'TimeStamp': timezone.now(), 'Mod': False}
                test.insert(data)
            MongoDBConnection().stop_connect()
    except():
        logging.info(u'Bleutrade parse mistake')
    logging.info(u'Bleutrade getticker ended')
