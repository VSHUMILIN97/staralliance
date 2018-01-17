# https://bleutrade.com/api/v2/public/getticker?market=ETH_BTC,LTC_BTC
import json
import logging
from django.utils import timezone
import requests
from mongo_db_connection import MongoDBConnection

pairlist = ['ETH_BTC', 'LTC_BTC', 'LTC_ETH', 'DASH_BTC']


def bleutrade_ticker():
    # Данные собираются для каждой валютной пары из списка pairlist
    logging.info(u'Bleutrade getticker started')
    try:
        #
        b = MongoDBConnection().start_db()
        db = b.PiedPiperStock
        test = db.BleutradeTick
        #
        for i in range(0, len(pairlist)):
            api_request = requests.get("https://bleutrade.com/api/v2/public/" + "getticker?market=" + pairlist[i])
            # Формируем JSON массив из данных с API
            json_data = json.loads(api_request.text)
            # Если все ок - парсим
            # Назначаем объект 'result' корневым, для простоты обращения
            root = json_data['result']
            bid, ask = float(root[0]['Bid']), float(root[0]['Ask'])
            #
            h = pairlist[i]
            if h == 'ETH_BTC':
                h = 'BTC-ETH'
            elif h == 'LTC_BTC':
                h = 'BTC-LTC'
            elif h == 'LTC_ETH':
                h = 'ETH-LTC'
            else:
                h = 'BTC-DASH'
            data = {'PairName': h, 'Tick': (ask+bid)/2, 'TimeStamp': timezone.now(), 'Mod': False}
            test.insert(data)
    except():
        logging.info(u'Bleutrade parse mistake')
    logging.info(u'Bleutrade getticker ended')