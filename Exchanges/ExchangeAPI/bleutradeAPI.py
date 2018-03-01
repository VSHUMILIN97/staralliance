# https://bleutrade.com/api/v2/public/getticker?market=ETH_BTC,LTC_BTC
import json
import logging
from django.utils import timezone
import requests
from Exchanges.data_model import ExchangeModel
from mongo_db_connection import MongoDBConnection


def pair_fix(pair_string):
    fixer = pair_string.split('_')
    pair_string = fixer[1] + '-' + fixer[0]
    return pair_string


def bleutrade_ticker():
    # Данные собираются для каждой валютной пары из списка pairlist
    global info_request, api_request
    logging.info(u'Bleutrade getticker started')
    try:
        #
        # b = MongoDBConnection().start_db()
        # db = b.PiedPiperStock
        # test = db.BleutradeTick
        #
        try:
            info_request = requests.get("https://bleutrade.com/api/v2/public/getmarkets")
        except ConnectionError:
            logging.error(u'Bleutrade info API cannot be reached')
        info_data = json.loads(info_request.text)
        data = info_data['result']
        pair_string = ""
        for each_index in range(0, len(data)):
            pair_string += data[each_index]['MarketName']
            if each_index + 1 != len(data):
                pair_string += ","
        try:
            api_request = requests.get("https://bleutrade.com/api/v2/public/" + "getticker?market=" + pair_string)
        except ConnectionError:
            logging.error(u'Bleutrade API cannot be reached')
        # Формируем JSON массив из данных с API. Проверяем код ответа.
        pair_array = pair_string.split(',')
        if api_request.status_code == 200:
            json_data = json.loads(api_request.text)
            # Если все ок - парсим
            # Назначаем объект 'result' корневым, для простоты обращения
            root = json_data['result']
            index = 0
            for item in root:
                ExchangeModel("Bleutrade", pair_fix(pair_array[index]), float(item['Bid']), float(item['Ask']))
               # # bid, ask = float(item['Bid']), float(item['Ask'])
               # #
               # data = {'PairName': pair_fix(pair_array[index]), 'Tick': (ask+bid)/2,
               #         'TimeStamp': timezone.now(), 'Mod': False}
               # test.insert(data)
                index = index + 1
        # MongoDBConnection().stop_connect()
    except OSError:
        logging.info(u'Bleutrade parse mistake')