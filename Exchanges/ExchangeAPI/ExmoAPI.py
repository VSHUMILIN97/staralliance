# https://api.exmo.com/v1/ticker/

import iso8601
import requests
import json
from django.utils import timezone
from mongo_db_connection import MongoDBConnection
import logging

pairlist = ['DASH_BTC', 'LTC_BTC', 'ETH_BTC', 'XRP_BTC', 'ETH_LTC']

def exmo_ticker():
    # Данные собираются для каждой валютной пары из списка pairlist
    # Получаем данные с API битрикса по конкретной валютной паре (ex. localhost/bittrex/btc-eth)
    logging.info(u'Exmo getticker started')
    #
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    test = db.ExmoTick
    #
    logging.info(u'Exmo getticker API was called')
    #
    for i in range(0, len(pairlist)):
        api_request = requests.get('https://api.exmo.com/v1/order_book/?pair=' + pairlist[i])
        # Формируем JSON массив из данных с API
        json_data = json.loads(api_request.text)
        # Если все ок - парсим
        root = json_data[pairlist[i]]
        # Назначаем объект 'result' корневым, для простоты обращения
        bid, ask = float(root['bid_top']), float(root['ask_top'])
        #
        h = ''
        if pairlist[i] == 'DASH_BTC':
            h = 'BTC-DASH'
        elif pairlist[i] == 'LTC_BTC':
            h = 'BTC-LTC'
        elif pairlist[i] == 'ETH_BTC':
            h = 'BTC-ETH'
        elif pairlist[i] == 'XRP_BTC':
            h = 'BTC-XRP'
        else:
            h = 'ETH-LTC'
        data = {'PairName': h, 'Tick': (ask+bid)/2, 'TimeStamp': timezone.now(), 'Mod': False}
        test.insert(data)
    logging.info(u'Exmo getticker ended')