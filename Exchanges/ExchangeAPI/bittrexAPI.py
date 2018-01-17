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
pairlist = ['BTC-1ST', 'BTC-LTC', 'BTC-ETH', 'BTC-DASH', 'BTC-XRP', 'ETH-LTC']

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

