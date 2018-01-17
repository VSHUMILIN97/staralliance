import json
import logging
from django.utils import timezone
import requests
from mongo_db_connection import MongoDBConnection

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


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


def livecoin_ticker():
    logging.info(u'livecoin getticker started')
    #
    try:
        ownpairlist = ['LTC/BTC', 'ETH/BTC', 'DASH/BTC']
        b = MongoDBConnection().start_db()
        db = b.PiedPiperStock
        test = db.LiveCoinTick
        #
        logging.info(u'livecoin getticker API was called')
        #a = '/exchange/ticker?currencyPair=LTC/BTC'
        for i in range(0, len(ownpairlist)):
            api_request = requests.get("https://api.livecoin.net" + "/exchange/ticker?currencyPair=" + ownpairlist[i])
            # Формируем JSON массив из данных с API
            json_data = json.loads(api_request.text)
            # Если все ок - парсим
            # Назначаем объект 'result' корневым, для простоты обращения
            root = json_data
            best_bid, best_ask = float(root['best_bid']), float(root['best_ask'])
            #
            a = ''
            if ownpairlist[i] == 'LTC/BTC':
                a = "BTC-LTC"
            elif ownpairlist[i] == 'ETH/BTC':
                a = "BTC-ETH"
            else:
                a = 'BTC-DASH'
            data = {'PairName': a, 'Tick': (best_ask + best_bid) / 2,
                    'TimeStamp': timezone.now(), 'Mod': False}
            test.insert(data)
        logging.info(u'livecoin getticker ended successfully')
    except:
        logging.error(u'Livecoin parse mistake')


#Ну собсна вот метод для LiveCoin, собирает всю полезную инфу , которая там есть.
#Метод разбавлен приятными строчками для дебага
#Вызывается в t5
#Боже, как же я люблю парсить
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
                    data = {'PairName': pair_name_formater(marketname), 'High': high, 'Low': low, 'Volume': volume,
                           'Last': last, 'TimeStamp': timezone.now(), 'Mod': False}
                    #Пишем только пары с USD, потому что можем
                    if (data['PairName'].find("-USD", 0, len(data['PairName']))) != -1:
                        test.insert(data)
                        #logging.info("WRITTEN - " + data['PairName'])


            logging.info(u'LiveCoin Data collected successfully')
    except:
        logging.info(u' LiveCoin collect all data Failed')
