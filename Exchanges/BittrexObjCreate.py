import iso8601
import requests
import json
from django.utils import timezone
from mongo_db_connection import MongoDBConnection
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

# Для чистоты кода используем переменные с названиями bit_obj_tick вместо bitObjTick
# В_питоне_модно_с_граундами_писать , а не с АпперКейсомТипВотТак
# Python != Java :'(((

# Вот эта беда должна быть огромных размеров, но девать нам её некуда особо, да и незачем. Надо собирать информацию.
# Ну и разумеется настало время try: catch: блоков. А то ху-о работает пока что, на соплях
pairlist = ['BTC-1ST', 'BTC-LTC', 'BTC-ETH']

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
    #logging.info(u'String ' + str(current_name) + " has been transformed into " + str(correct_name))
    return correct_name

# Метод получается последние биржевые данные, парсит поля и выносит в модель необходимое.
def api_get_getmarketsummaries():
    logging.info(u'Bittrex getsummaries started')
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    test = db.Bittrex
    api_request = requests.get("https://bittrex.com/api/v1.1/public/" + "getmarketsummaries")
    json_data = json.loads(api_request.text)
    #
    logging.info(u'Bittrex getsummaries API was called')
    #
    # Если полученный JSON массив из apiRequest несет в себе данные , а не разочарование , то , парсим по переменным
    # и передаем все это в новый объект из models.py
    # Для timestamp используем формат ISO8601, который DateTime модели без проблем распознает =)

    if json_data['success']:
        result = json_data['result']

        for item in result:
            marketname, high, low, volume, last, basevolume, timestamp,\
            bid, ask, openbuyorders, opensellorders, prevday = \
             str(item['MarketName']), float('{:.10f}'.format(item['High'])), float('{:.10f}'.format(item['Low'])), \
             float('{:.10f}'.format(item['Volume'])), float('{:.10f}'.format(item['Last'])),\
             float('{:.10f}'.format(item['BaseVolume'])), \
             iso8601.parse_date(item['TimeStamp']), float('{:.10f}'.format(item['Bid'])),\
             float('{:.10f}'.format(item['Ask'])), str(item['OpenBuyOrders']),\
             str(item['OpenSellOrders']), float('{:.10f}'.format(item['PrevDay']))
            # Формируем словарь из значений
            data = {'PairName': marketname, 'High': high, 'Low': low, 'Last': last,
                    'PrevDay': prevday, 'TimeStamp': timestamp, 'Mod': False}
            test.insert(data)
    logging.info(u'Bittrex getsummaries ended')


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
    logging.info(u'Bittrex getticker API was called')
    #
    for i in range(0, len(pairlist)):
        api_request = requests.get("https://bittrex.com/api/v1.1/public/" + "getticker?market=" + pairlist[i])
        # Формируем JSON массив из данных с API
        json_data = json.loads(api_request.text)
        # Если все ок - парсим
        if json_data['success']:

            # Назначаем объект 'result' корневым, для простоты обращения
            root = json_data['result']
            bid, ask, last = float(root['Bid']), float(root['Ask']), str(root['Last'])
            #
            data = {'PairName': pairlist[i], 'Tick': (ask+bid)/2, 'TimeStamp': timezone.now(), 'Mod': False}
            test.insert(data)
    logging.info(u'Bittrex getticker ended')


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

            for item in result:
                iD, timestamp, quantity, price, total, filltype, ordertype = \
                    int(item['Id']), iso8601.parse_date(item['TimeStamp']), float(item['Quantity']),\
                    float(item['Price']), float(item['Total']),\
                    str(item['FillType']), str(item['OrderType'])
                #
                data = {'PairName': pairlist[i], 'OrderID': iD, 'Quantity': quantity, 'Price': price, 'Total': total,
                        'FillType': filltype, 'OrderType': ordertype, 'TimeStamp': timestamp, 'Mod': False}
                test.insert(data)
    logging.info(u'Bittrex getmarkethistory ended')


def livecoin_ticker():
    logging.info(u'livecoin getticker started')
    #
    try:
        ownpairlist = ['LTC/BTC', 'ETH/BTC']
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
            if ownpairlist[i] == 'LTC/BTC':
                a = "BTC-LTC"
            else:
                a = "BTC-ETH"
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
    except:
        logging.error(r'gatecoin ticker mistake')