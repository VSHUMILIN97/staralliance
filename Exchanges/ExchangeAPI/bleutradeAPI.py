# https://bleutrade.com/api/v2/public/getticker?market=ETH_BTC,LTC_BTC
import json
import logging
from django.utils import timezone
import requests
from mongo_db_connection import MongoDBConnection

pairlist = 'ETH_BTC,LTC_BTC,LTC_ETH,DASH_BTC'


def pair_fix(pair_string):
    return str(pair_string).replace('_', '-')


def bleutrade_ticker():
    # Данные собираются для каждой валютной пары из списка pairlist
    logging.info(u'Bleutrade getticker started')
    try:
        #
        b = MongoDBConnection().start_db()
        db = b.PiedPiperStock
        test = db.BleutradeTick
        #
        api_request = requests.get("https://bleutrade.com/api/v2/public/" + "getticker?market=" + pairlist)
        # Формируем JSON массив из данных с API. Проверяем код ответа.
        logging.info('Bleutrade API returned - ' + str(api_request.status_code))
        if api_request.status_code == 200:
            json_data = json.loads(api_request.text)
            # Если все ок - парсим
            # Назначаем объект 'result' корневым, для простоты обращения
            root = json_data['result']
            index = 0
            for item in root:
                bid, ask = float(item['Bid']), float(item['Ask'])
                #
                data = {'PairName': pair_fix(pairlist.split(',')[index]), 'Tick': (ask+bid)/2,
                        'TimeStamp': timezone.now(), 'Mod': False}
                test.insert(data)
                index = index + 1
        MongoDBConnection().stop_connect()
    except():
        logging.info(u'Bleutrade parse mistake')
    logging.info(u'Bleutrade getticker ended')
