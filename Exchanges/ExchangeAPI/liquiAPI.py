# https://api.liqui.io/api/3/depth/ltc_btc?limit=1
import json
import logging
from django.utils import timezone
import requests
from mongo_db_connection import MongoDBConnection

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


def liqui_ticker():
    global best_ask, best_bid
    logging.info(u'Liqui getticker started')
    #
    try:
        ownpairlist = ['eth_btc', 'ltc_btc', 'dash_btc', 'ltc_eth']
        b = MongoDBConnection().start_db()
        db = b.PiedPiperStock
        release = db.LiquiTick
        #
        for i in range(0, len(ownpairlist)):
            api_request = requests.get("https://api.liqui.io" + "/api/3/depth/" + ownpairlist[i] + '?limit=1')
            # Формируем JSON массив из данных с API
            json_data = json.loads(api_request.text)
            # Если все ок - парсим
            root = json_data[ownpairlist[i]]
            best_ask = root['asks'][0][0]
            best_bid = root['bids'][0][0]
            #
            a = ''
            if ownpairlist[i] == 'eth_btc':
                a = "BTC-ETH"
            elif ownpairlist[i] == 'ltc_btc':
                a = "BTC-LTC"
            elif ownpairlist[i] == 'dash_btc':
                a = 'BTC-DASH'
            else:
                a = 'ETH-LTC'
            data = {'PairName': a, 'Tick': (best_ask + best_bid) / 2,
                    'TimeStamp': timezone.now(), 'Mod': False}
            release.insert(data)
        logging.info(u'Liqui getticker ended successfully')
    except():
        logging.error(u'Liqui parse mistake')