# https://api.gatecoin.com/Public/LiveTickers
import json
import logging
from django.utils import timezone
import requests
from mongo_db_connection import MongoDBConnection

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


# Боевая задачка - написать неунифицированные парсилки пар, чтобы все совпадало. Без хардкода.
def pair_name_formater(current_name):
    symbols_collection = ['/', '_'] #to be continued
    for symbol in symbols_collection:
        if current_name.find(symbol):
            correct_name = current_name.replace(str(symbol), '-')
            #logging.info("FOUND MATCH -- " + symbol)
            break
    correct_name = correct_name.upper()
    # if correct_name == 'LTC-BTC':
    #    correct_name = 'BTC-LTC'
    # logging.info(u'String ' + str(current_name) + " has been transformed into " + str(correct_name))
    return correct_name


def gatecoin_ticker():
    logging.info(u'Gatecoin collection of data in parse')

    try:
        b = MongoDBConnection().start_db()
        db = b.PiedPiperStock
        gcstock = db.GatecoinTick
        api_request = requests.get("https://api.gatecoin.com/Public/LiveTickers")
        json_data = json.loads(api_request.text)


        result = json_data['tickers']
        for item in result:
            if item['currencyPair'] == 'ETHBTC':
                market, bid, ask = str(item['currencyPair']), float(item['bid']), float(item['ask'])
                a = market.replace('ETHBTC', 'BTC-ETH')
                data = {'PairName': a, 'Tick': (bid + ask)/2, 'TimeStamp': timezone.now(), 'Mod': False}
                gcstock.insert(data)
            elif item['currencyPair'] == '1STBTC':
                market, bid, ask = str(item['currencyPair']), float(item['bid']), float(item['ask'])
                b = market.replace('1STBTC', 'BTC-1ST')
                data = {'PairName': b, 'Tick': (bid + ask) / 2, 'TimeStamp': timezone.now(), 'Mod': False}
                gcstock.insert(data)
            elif item['currencyPair'] == 'LTCBTC':
                market, bid, ask = str(item['currencyPair']), float(item['bid']), float(item['ask'])
                h = market.replace('LTCBTC', 'BTC-LTC')
                data = {'PairName': h, 'Tick': (bid + ask) / 2, 'TimeStamp': timezone.now(), 'Mod': False}
                gcstock.insert(data)
    except():
        logging.error(r'gatecoin ticker mistake')