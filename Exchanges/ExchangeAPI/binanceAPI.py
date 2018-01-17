# https://www.binance.com/api/v3/ticker/bookTicker
import json
import logging
from django.utils import timezone
import requests
from mongo_db_connection import MongoDBConnection

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


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
        json_data = json.loads(api_request.text)
        # Если все ок - парсим
        root = json_data
        for item in root:
            if item['symbol'] == 'ETHBTC':
                bid, ask = float(item['bidPrice']), float(item['askPrice'])
                data = {'PairName': 'BTC-ETH', 'Tick': (ask + bid) / 2, 'TimeStamp': timezone.now(), 'Mod': False}
                release.insert(data)
            elif item['symbol'] == 'LTCBTC':
                bid, ask = float(item['bidPrice']), float(item['askPrice'])
                data = {'PairName': 'BTC-LTC', 'Tick': (ask + bid) / 2, 'TimeStamp': timezone.now(), 'Mod': False}
                release.insert(data)
            elif item['symbol'] == 'LTCETH':
                bid, ask = float(item['bidPrice']), float(item['askPrice'])
                data = {'PairName': 'ETH-LTC', 'Tick': (ask + bid) / 2, 'TimeStamp': timezone.now(), 'Mod': False}
                release.insert(data)
            elif item['symbol'] == 'DASHBTC':
                bid, ask = float(item['bidPrice']), float(item['askPrice'])
                data = {'PairName': 'BTC-DASH', 'Tick': (ask + bid) / 2, 'TimeStamp': timezone.now(), 'Mod': False}
                release.insert(data)
            elif item['symbol'] == 'XRPBTC':
                bid, ask = float(item['bidPrice']), float(item['askPrice'])
                data = {'PairName': 'BTC-XRP', 'Tick': (ask + bid) / 2, 'TimeStamp': timezone.now(), 'Mod': False}
                release.insert(data)
            else:
                continue
            logging.info(u'Binance getticker ended successfully')
    except():
        logging.error(u'Binance parse mistake')