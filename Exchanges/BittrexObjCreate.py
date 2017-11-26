import datetime
import iso8601
import pytz
import requests
import json
from django.utils import timezone
import time
from Exchanges.views import BittrexOHLC
from Exchanges.views import BittrexTick
from Exchanges.views import BittrexVolume

# Для чистоты кода используем переменные с названиями bit_obj_tick вместо bitObjTick
# В_питоне_модно_с_граундами_писать , а не с АпперКейсомТипВотТак
# Python != Java :'(((

pairlist = ['BTC-1ST', 'BTC-LTC', 'BTC-ETH']

def api_get_getmarketsummaries():
    timezone.deactivate()
    print('Before Bittrix call attempt to server - ' + str(time.time()))

    api_request = requests.get("https://bittrex.com/api/v1.1/public/" + "getmarketsummaries")
    json_data = json.loads(api_request.text)

    print("api get.Bittrix is called - " + str(time.time()))

    # Если полученный JSON массив из apiRequest несет в себе данные , а не разочарование , то , парсим по переменным
    # и передаем все это в новый объект из models.py
    # Для timestamp используем формат ISO8601, который DateTime модели без проблем распознает =)

    if json_data['success']:
        result = json_data['result']

        for item in result:
            marketname, high, low, volume, last, basevolume, timestamp, bid, ask, openbuyorders, opensellorders, prevday = \
             str(item['MarketName']), float('{:.10f}'.format(item['High'])), float('{:.10f}'.format(item['Low'])), \
             float('{:.10f}'.format(item['Volume'])), float('{:.10f}'.format(item['Last'])), float('{:.10f}'.format(item['BaseVolume'])), \
             iso8601.parse_date(item['TimeStamp']), float('{:.10f}'.format(item['Bid'])),\
             float('{:.10f}'.format(item['Ask'])), str(item['OpenBuyOrders']),\
             str(item['OpenSellOrders']), float('{:.10f}'.format(item['PrevDay']))

            # Создаем объект типа BittrexOHLC ( models.py ) и в конструктор передаем результаты обращения к API

            bit_obj_ohlc = BittrexOHLC(PairName=marketname, High=high, Low=low,
                                       Last=last, TimeStamp=timestamp, PrevDay=prevday)
            bit_obj_ohlc.save()


def api_get_getticker():

     # Доделал под текущую вьюху
    # Получаем данные с API битрикса по конкретной валютной паре (ex. localhost/bittrex/btc-eth
    for i in range(0, len(pairlist)):
        api_request = requests.get("https://bittrex.com/api/v1.1/public/" + "getticker?market=" + pairlist[i])
        # Формируем JSON массив из данных с API
        json_data = json.loads(api_request.text)
        # Если все ок - парсим
        if json_data['success']:

            # Назначаем объект 'result' корневым, для простоты обращения
            root = json_data['result']
            bid, ask, last = float(root['Bid']), float(root['Ask']), str(root['Last'])

            # Создаем объект по модели BittrexTick , в конструктор передаем распаршенные данные
            bit_obj_tick = BittrexTick(PairName=pairlist[i], Tick=((ask + bid) / 2))
            bit_obj_tick.save()
            print('Ended getticker['+str(i)+'] in - ', str(time.time()))


def api_get_getmarkethistory():

    for i in range(0, len(pairlist)):
        api_request = requests.get("https://bittrex.com/api/v1.1/public/" + "getmarkethistory?market=" + pairlist[i])
        json_data = json.loads(api_request.text)
        if json_data['success']:
            result = json_data['result']
            for item in result:
                iD, timestamp, quantity, price, total, filltype, ordertype = \
                int(item['Id']), iso8601.parse_date(item['TimeStamp']), float(item['Quantity']), float(item['Price']), float(item['Total']), str(item['FillType']), str(item['OrderType'])

                bit_obj_vol = BittrexVolume(PairName=pairlist[i], IdOrder=iD, TimeStamp=timestamp, Quantity=quantity, Price=price, Total=total, FillType=filltype, OrderType=ordertype)
                bit_obj_vol.save()

###Рабочая версия парсилки с датами
"""
 if json_data['success']:
        result = json_data['result']

        for item in result:
            marketname, high, low, volume, last, basevolume, timestamp, bid, ask, openbuyorders, opensellorders, prevday = \
             str( item['MarketName']), float('{:.10f}'.format( item['High'])), float('{:.10f}'.format(item['Low'])), \
             float('{:.10f}'.format(item['Volume'])), float('{:.10f}'.format( item['Last'])), float('{:.10f}'.format(item['BaseVolume'])), \
             (str(item['TimeStamp']).replace('T', ',').replace(':', ',').replace('-', ',').replace('.', ',')).split(','), float('{:.10f}'.format( item['Bid'])),\
             float( '{:.10f}'.format(item['Ask'])), str(item['OpenBuyOrders']), str(item['OpenSellOrders']), float('{:.10f}'.format(item['PrevDay']))

            # Создаем объект типа BittrexOHLC ( models.py ) и в конструктор передаем результаты обращения к API
            dtutc = datetime.datetime(int(timestamp[0]), int(timestamp[1]), int(timestamp[2]), int(timestamp[3]), int(timestamp[4]), int(timestamp[5]), tzinfo=pytz.UTC)
            bit_obj_ohlc = BittrexOHLC(PairName=marketname, High=high, Low=low, Last=last,
                                 Volume=volume, BaseVolume=basevolume,
                                 TimeStamp=dtutc, Bid=bid, Ask=ask, OpenBuyOrders=openbuyorders,
                                 OpenSellOrders=opensellorders, PrevDay=prevday)
            bit_obj_ohlc.save()
"""