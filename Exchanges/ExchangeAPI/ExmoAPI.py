# https://api.exmo.com/v1/ticker/
import asyncio
from datetime import datetime
import dateutil.parser
import iso8601
import pymongo
import requests
import json
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../cryptopiper'))
from PiedPiper.settings import STARALLIANS_HOST, REDIS_DEFAULT_PORT
from django.utils import timezone
from mongo_db_connection import MongoDBConnection
import logging
import redis


logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename='/var/log/cryptopiper/exmoAPI.log')

conn_r = redis.ConnectionPool(host=STARALLIANS_HOST, port=REDIS_DEFAULT_PORT, db=0)
r = redis.Redis(connection_pool=conn_r)

pairlist = ['DASH_BTC', 'LTC_BTC', 'ETH_BTC', 'XRP_BTC', 'ETH_LTC']


def pair_fix(pair_string):
    fixer = pair_string.split('_')
    pair_string = fixer[1] + '-' + fixer[0]
    return pair_string


def exmo_charts_data():
    global lurktime_exmo
    b = MongoDBConnection().start_local()
    db = b.PiedPiperStock
    test = db.Exmo
    logging.info(u'Exmo getsummaries API was called')
    for i in range(0, len(pairlist)):
        api_request = requests.get("https://api.exmo.me/v1/trades/?pair=" + pairlist[i])
        json_data = json.loads(api_request.text)

        lurktime_exmo = None
        # Если полученный JSON массив из apiRequest несет в себе данные , а не разочарование , то , парсим по переменным
        # и передаем все это в новый объект из models.py
        # Для timestamp используем формат ISO8601, который DateTime модели без проблем распознает =)
        time_after_aggregation = test.find({'PairName': pair_fix(pairlist[i]), 'Mod': False},
                                           {'TimeStamp': True}).sort('TimeStamp', pymongo.DESCENDING).limit(1)
        #
        for subintosub in time_after_aggregation:
            lurktime_exmo = dateutil.parser.parse(str(subintosub['TimeStamp']))

        result = json_data[pairlist[i]]

        for item in result:
            if lurktime_exmo is None:
                        timestamp, price = \
                            iso8601.parse_date(str(datetime.fromtimestamp(item['date'], tz=timezone.utc).isoformat())),\
                            float(item['price'])
                        #
                        data = {'PairName': pair_fix(pairlist[i]), 'Price': price, 'TimeStamp': timestamp,
                                'Mod': False}
                        test.insert(data)
            elif lurktime_exmo < iso8601.parse_date(datetime.fromtimestamp((item['date'])).isoformat())\
                    .replace(tzinfo=None):
                        timestamp, price = \
                            iso8601.parse_date(str(datetime.fromtimestamp(item['date'], tz=timezone.utc).isoformat())),\
                            float(item['price'])
                        #
                        data = {'PairName': pair_fix(pairlist[i]), 'Price': price, 'TimeStamp': timestamp,
                                'Mod': False}
                        test.insert(data)
            else:
                        continue
    MongoDBConnection().stop_connect()
    logging.info(u'EXMO charts data aggregation ended')


async def exmo_ticker():
    # Данные собираются для каждой валютной пары из списка pairlist
    # Получаем данные с API битрикса по конкретной валютной паре (ex. localhost/bittrex/btc-eth)
    global data, api_request
    import os
    file_name = os.path.basename(sys.argv[0]).replace('.py', '')
    logging.info(u'Exmo getticker started')
    while 1:
        try:
            try:
                api_request = requests.get("https://api.exmo.me/v1/ticker/")
            except ConnectionError:
                logging.error(u'Exmo API cannot be reached')
            # Проверяем ответ на вшивость. Если код не 200, то данные не записываем.
            if api_request.status_code == 200:
                # Формируем JSON массив из данных с API
                json_data = json.loads(api_request.text)
                # Если все ок - парсим
                for item in json_data:
                    main_key = file_name + '/Exmo/' + pair_fix(item)
                    if r.get(main_key) is None:
                        r.set(main_key, 1)
                    if float(r.get(file_name + '/Exmo/' +
                                   pair_fix(item)).decode('utf-8')) != (float(json_data[item]['buy_price']) +
                                                                        float(json_data[item]['sell_price']))/2:
                        r.set(file_name + '/Exmo/' + pair_fix(item),
                              (float(json_data[item]['buy_price']) + float(json_data[item]['sell_price'])) / 2)
                        r.publish('s-Exmo', file_name + '/Exmo/' + pair_fix(item))
                        await asyncio.sleep(18 / 46)
                    else:
                        await asyncio.sleep(18 / 46)
                        continue
        except OSError:
            logging.error('No internet connection on EXMO')
            continue


def exmo_volume_data():
    # Данные собираются для каждой валютной пары из списка pairlist
    logging.info(u'Bittrex getmarkethistory started')
    #
    b = MongoDBConnection().start_local()
    db = b.PiedPiperStock
    test = db.ExmoMHist
    #
    logging.info(u'Exmo volume API aggregator  was called')
    #
    for i in range(0, len(pairlist)):
            api_request = requests.get("https://api.exmo.me/v1/trades/?pair=" + pairlist[i])
            json_data = json.loads(api_request.text)

            result = json_data[pairlist[i]]

            for item in result:
                timestamp, quantity, price, ordertype = \
                    iso8601.parse_date(str(datetime.fromtimestamp(item['date'], tz=timezone.utc).isoformat())),\
                    float(item['quantity']), float(item['price']), str(item['type']).upper()
                #
                data = {'PairName': pair_fix(pairlist[i]), 'Quantity': quantity, 'Price': price,
                        'OrderType': ordertype, 'TimeStamp': timestamp, 'Mod': False}
                test.insert(data)
    MongoDBConnection().stop_connect()
    logging.info(u'Exmo volume aggregation ended')


loop = asyncio.get_event_loop()
loop.run_until_complete(exmo_ticker())
loop.run_forever()