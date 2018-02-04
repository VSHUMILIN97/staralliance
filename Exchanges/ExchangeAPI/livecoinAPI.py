import json
import logging
from django.utils import timezone
import requests
from mongo_db_connection import MongoDBConnection

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

def pair_fix(pair_string):
    return str(pair_string).replace('/', '-')


def livecoin_ticker():
    logging.info(u'livecoin getticker started')
    #
    ownpairlist = ['LTC/BTC', 'ETH/BTC', 'DASH/BTC']
    #
    try:
        b = MongoDBConnection().start_db()
        db = b.PiedPiperStock
        test = db.LiveCoinTick
        #
        logging.info(u'livecoin getticker API was called')
        # a = '/exchange/ticker?currencyPair=LTC/BTC'
        api_request = requests.get("https://api.livecoin.net" + "/exchange/ticker")
        logging.info('Livecoin API returned - ' + str(api_request.status_code))
        if api_request.status_code == 200:
            # Формируем JSON массив из данных с API
            json_data = json.loads(api_request.text)
            # Если все ок - парсим
            for item in json_data:
                if item['symbol'] in ownpairlist:
                    # Назначаем объект 'result' корневым, для простоты обращения
                    best_bid, best_ask = float(item['best_bid']), float(item['best_ask'])

                    data = {'PairName': pair_fix(item['symbol']), 'Tick': (best_ask + best_bid) / 2,
                            'TimeStamp': timezone.now(), 'Mod': False}
                    test.insert(data)
        logging.info(u'Livecoin getticker ended successfully')
        MongoDBConnection().stop_connect()
    except():
        logging.error(u'Livecoin parse mistake')


# Ну собсна вот метод для LiveCoin, собирает всю полезную инфу , которая там есть.
# Метод разбавлен приятными строчками для дебага
# Вызывается в t5
# Боже, как же я люблю парсить
def livecoin_ticker_all_info():
    logging.info(u'LiveCoin collect all data started')

    try:
        b = MongoDBConnection().start_db()
        db = b.PiedPiperStock
        test = db.LiveCoin
        api_request = requests.get("https://api.livecoin.net/exchange/ticker")
        # Формируем JSON массив из данных с API
        json_data = json.loads(api_request.text)
        # Если все ок - парсим
        # Назначаем объект 'result' корневым, для простоты обращения

        for item in json_data:

                #logging.info("COUNT TEST " + item['symbol'] + " --- " + str(i))
                marketname, high, low , volume , last = item['symbol'] , \
                                                        float('{:.10f}'.format(item['high'])) ,\
                                                        float('{:.10f}'.format(item['low'])),\
                                                        float('{:.10f}'.format(item['volume'])),\
                                                        float('{:.10f}'.format(item['last']))

                #logging.info("LIVECOIN TEST: ___" + marketname + "  -  " + str(high) + "
                # -  " + str(low)+ "  -  " + str(volume) + "  -  " + str(last) )
                data = {'PairName': pair_fix(marketname), 'High': high, 'Low': low, 'Volume': volume,
                       'Last': last, 'TimeStamp': timezone.now(), 'Mod': False}
                #Пишем только пары с USD, потому что можем
                if (data['PairName'].find("-USD", 0, len(data['PairName']))) != -1:
                    test.insert(data)
                    #logging.info("WRITTEN - " + data['PairName'])


        logging.info(u'LiveCoin Data collected successfully')
        MongoDBConnection().stop_connect()
    except():
        logging.info(u' LiveCoin collect all data Failed')
