import iso8601
import pymongo
import requests
import json
import dateutil.parser
from django.utils import timezone
from datetime import timedelta
from mongo_db_connection import MongoDBConnection
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename='/var/log/cryptopiper/DataParser.log')

# Для чистоты кода используем переменные с названиями bit_obj_tick вместо bitObjTick
# В_питоне_модно_с_граундами_писать , а не с АпперКейсомТипВотТак
# Python != Java :'(((

# Вот эта беда должна быть огромных размеров, но девать нам её некуда особо, да и незачем. Надо собирать информацию.
# Ну и разумеется настало время try: catch: блоков. А то ху-о работает пока что, на соплях
pairlist = ['BTC-1ST', 'BTC-LTC', 'BTC-ETH', 'BTC-DASH', 'BTC-XRP', 'ETH-LTC']


def pair_fix(pair_string):
    if str(pair_string).split('-')[0] == 'BTC' or 'ETH':
        a = str(pair_string).split('-')[0]
        b = str(pair_string).split('-')[1]
        c = b + "-" + a
        return c
    else:
        return pair_string


# Метод получается последние биржевые данные, парсит поля и выносит в модель необходимое.
# https://bittrex.com/api/v1.1/public/getmarkethistory?market=BTC-LTC
def api_get_getmarketsummaries():
    global lurktime
    logging.info(u'Bittrex getsummaries started')
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    test = db.Bittrex
    for i in range(0, len(pairlist)):
        api_request = requests.get("https://bittrex.com/api/v1.1/public/" + "getmarkethistory?market=" + pairlist[i])
        json_data = json.loads(api_request.text)
        #
        logging.info(u'Bittrex getsummaries API was called')
        #
        lurktime = None
        # Если полученный JSON массив из apiRequest несет в себе данные , а не разочарование , то , парсим по переменным
        # и передаем все это в новый объект из models.py
        # Для timestamp используем формат ISO8601, который DateTime модели без проблем распознает =)
        time_after_aggregation = test.find({'PairName': pair_fix(pairlist[i]), 'Mod': False},
                                           {'TimeStamp': True}).sort('TimeStamp', pymongo.DESCENDING).limit(1)

        for subintosub in time_after_aggregation:
            lurktime = dateutil.parser.parse(str(subintosub['TimeStamp']))

        if json_data['success']:
            result = json_data['result']

            for item in result:
                if lurktime is None:
                    timestamp, price = \
                        iso8601.parse_date(item['TimeStamp']), float(item['Price'])
                    #
                    data = {'PairName': pair_fix(pairlist[i]), 'Price': price, 'TimeStamp': timestamp,
                            'Mod': False}
                    test.insert(data)
                elif lurktime < iso8601.parse_date(item['TimeStamp']).replace(tzinfo=None):
                    timestamp, price = \
                     iso8601.parse_date(item['TimeStamp']),  float(item['Price'])
                    #
                    data = {'PairName': pair_fix(pairlist[i]), 'Price': price, 'TimeStamp': timestamp,
                            'Mod': False}
                    test.insert(data)
                else:
                    continue
        logging.info(u'Bittrex getsummaries ended')
    MongoDBConnection().stop_connect()


# По некоторым соображениям, самый работающий график на данный момент.
# Получает данные на текущий момент. В models указан default для TimeStamp timezone.now
# Указаний по TimeStamp НЕ ТРЕБУЕТСЯ
def api_get_getticker():
    # Данные собираются для каждой валютной пары из списка pairlist
    # Получаем данные с API битрикса по конкретной валютной паре (ex. localhost/bittrex/btc-eth)
    logging.info(u'Bittrex getticker started')
    #
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    test = db.BittrexTick
    #
    api_request = requests.get("https://bittrex.com/api/v1.1/public/" + "getmarketsummaries")
    #
    logging.info('Bittrex API returned - ' + str(api_request.status_code))
    if api_request.status_code == 200:
        json_data = json.loads(api_request.text)
        # Если все ок - парсим
        if json_data['success']:
            # Назначаем объект 'result' корневым, для простоты обращения
            root = json_data['result']
            for item in root:
                if item['MarketName'] in pairlist:
                    bid, ask = float(item['Bid']), float(item['Ask'])
                    #
                    data = {'PairName': pair_fix(item['MarketName']), 'Tick': (ask+bid)/2,
                            'TimeStamp': timezone.now(), 'Mod': False}
                    test.insert(data)
    logging.info(u'Bittrex getticker ended')
    MongoDBConnection().stop_connect()


# Получаем все сделки за некоторое(б-гу известное) время.
# Из реальных минусов - TimeStamp в каком-то хаотичном порядке
def api_get_getmarkethistory():
    # Данные собираются для каждой валютной пары из списка pairlist
    logging.info(u'Bittrex getmarkethistory started')
    #
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    test = db.BittrexMHist
    #
    logging.info(u'Bittrex getmarkethistory API was called')
    #
    for i in range(0, len(pairlist)):
        api_request = requests.get("https://bittrex.com/api/v1.1/public/" + "getmarkethistory?market=" + pairlist[i])
        json_data = json.loads(api_request.text)
        if json_data['success']:
            result = json_data['result']

            if result:
                for item in result:
                    timestamp, quantity, price, ordertype = \
                        iso8601.parse_date(item['TimeStamp']), float(item['Quantity']),\
                        float(item['Price']), str(item['OrderType'])
                    #
                    data = {'PairName': pair_fix(pairlist[i]), 'Quantity': quantity, 'Price': price,
                            'OrderType': ordertype, 'TimeStamp': timestamp, 'Mod': False}
                    test.insert(data)
                    
    logging.info(u'Bittrex getmarkethistory ended')
    MongoDBConnection().stop_connect()

