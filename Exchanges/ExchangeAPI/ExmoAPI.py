# https://api.exmo.com/v1/ticker/

import iso8601
import requests
import json
from django.utils import timezone
from mongo_db_connection import MongoDBConnection
import logging

pairlist = 'DASH_BTC,LTC_BTC,ETH_BTC,XRP_BTC,ETH_LTC'


def pair_fix(pair_string):
    return str(pair_string).replace('_', '-')


def exmo_ticker():
    # Данные собираются для каждой валютной пары из списка pairlist
    # Получаем данные с API битрикса по конкретной валютной паре (ex. localhost/bittrex/btc-eth)
    global data
    logging.info(u'Exmo getticker started')
    #
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    test = db.ExmoTick
    #
    logging.info(u'Exmo getticker API was called')
    #
    api_request = requests.get('https://api.exmo.me/v1/order_book/?pair=' + pairlist)
    # Проверяем ответ на вшивость. Если код не 200, то данные не записываем.
    logging.info('Exmo API returned - ' + str(api_request.status_code))
    if api_request.status_code == 200:
        # Формируем JSON массив из данных с API
        json_data = json.loads(api_request.text)
        # Если все ок - парсим
        for item in json_data:
            bid, ask = float(json_data[item]['bid_top']), float(json_data[item]['ask_top'])
            data = {'PairName': pair_fix(item), 'Tick': (ask+bid)/2, 'TimeStamp': timezone.now(), 'Mod': False}
            test.insert(data)
    logging.info(u'Exmo getticker ended')
