import iso8601
import pymongo
import requests
import json
import dateutil.parser
import asyncio
import redis
import logging
logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename='/var/log/cryptopiper/bittrexAPI.log')
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../cryptopiper'))
from PiedPiper.settings import STARALLIANS_HOST, REDIS_DEFAULT_PORT, LOCAL_SERVICE_HOST
from mongo_db_connection import MongoDBConnection


conn_r = redis.ConnectionPool(host=STARALLIANS_HOST, port=REDIS_DEFAULT_PORT, db=0)
r = redis.Redis(connection_pool=conn_r)

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
    b = MongoDBConnection().start_local()
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
async def api_get_getticker():
    # Данные собираются для каждой валютной пары из списка pairlist
    # Получаем данные с API битрикса по конкретной валютной паре (ex. localhost/bittrex/btc-eth)
    global api_request
    import os
    file_name = os.path.basename(sys.argv[0]).replace('.py', '')
    logging.info(u'Bittrex getticker started')
    while 1:
        try:
            try:
                api_request = requests.get("https://bittrex.com/api/v1.1/public/" + "getmarketsummaries")
            except ConnectionError:
                logging.error(u'Bittrex API cannot be reached')
            #
            if api_request.status_code == 200:
                json_data = json.loads(api_request.text)
                # Если все ок - парсим
                if json_data['success']:
                    # Назначаем объект 'result' корневым, для простоты обращения
                    root = json_data['result']
                    for item in root:
                        main_key = file_name + '/Bittrex/' + item['MarketName']
                        if r.get(main_key) is None:
                            r.set(main_key, 1)
                        if float(r.get(main_key).decode('utf-8')) != (float(item['Bid']) + float(item['Ask']))/2:
                            r.set(main_key, (float(item['Bid']) + float(item['Ask'])) / 2)
                            r.publish('s-Bittrex', main_key)
                            await asyncio.sleep(16/270)
                        else:
                            await asyncio.sleep(16/270)
                            continue
        except OSError:
            logging.error('NO INTERNET CONNECTION')
            continue


# Получаем все сделки за некоторое(б-гу известное) время.
# Из реальных минусов - TimeStamp в каком-то хаотичном порядке
def api_get_getmarkethistory():
    # Данные собираются для каждой валютной пары из списка pairlist
    logging.info(u'Bittrex getmarkethistory started')
    #
    b = MongoDBConnection().start_local()
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


loop = asyncio.get_event_loop()
loop.run_until_complete(api_get_getticker())
loop.run_forever()