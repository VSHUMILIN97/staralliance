# https://www.binance.com/api/v3/ticker/bookTicker
import json
import logging
from django.utils import timezone
import requests
from mongo_db_connection import MongoDBConnection

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)
pairlist = ['ETHBTC', 'LTCBTC', 'LTCETH', 'DASHBTC', 'XRPBTC']
coins = ['ETH', 'BTC', 'LTC', 'DASH', 'XRP', '1ST']


def pair_fix(pair_string):
    for i in range(0, len(coins)):
        if str(pair_string).startswith(coins[i]) is True:
            return str(pair_string).replace(coins[i], coins[i]+'-')


def binance_ticker():
    logging.info(u'Binance getticker started')
    #
    try:
        b = MongoDBConnection().start_db()
        db = b.PiedPiperStock
        release = db.BinanceTick
        #
        api_request = requests.get("https://www.binance.com/api/" + "v3/ticker/bookTicker")
        # Формируем JSON массив из данных с API
        logging.info('Binance API returned - ' + str(api_request.status_code))
        if api_request.status_code == 200:
            json_data = json.loads(api_request.text)
            # Если все ок - парсим
            for item in json_data:
                if item['symbol'] in pairlist:
                    bid, ask = float(item['bidPrice']), float(item['askPrice'])
                    data = {'PairName': pair_fix(item['symbol']), 'Tick': (ask + bid) / 2,
                            'TimeStamp': timezone.now(), 'Mod': False}
                    release.insert(data)
                else:
                    continue
            logging.info(u'Binance getticker ended successfully')
        MongoDBConnection().stop_connect()
    except():
        logging.error(u'Binance parse mistake')