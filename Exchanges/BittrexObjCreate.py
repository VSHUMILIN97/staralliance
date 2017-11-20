import datetime

import requests
import json
import time
from Exchanges.views import BittrexOHLC
from Exchanges.views import BittrexTick

def api_get_getmarketsummaries():
    print('Before Bittrix call attempt to server - ' + str(time.time()))
    apiRequest = requests.get("https://bittrex.com/api/v1.1/public/" + "getmarketsummaries")
    json_data = json.loads(apiRequest.text)
    print("api get.Bittrix is called - " + str(time.time()))
    if json_data['success']:
        result = json_data['result']
        for item in result:
            marketname, high, low, volume, last, basevolume, timestamp, bid, ask, openbuyorders, opensellorders, prevday = \
             str( item['MarketName']), float('{:.10f}'.format( item['High'])), float('{:.10f}'.format(item['Low'])), \
             float('{:.10f}'.format(item['Volume'])), float('{:.10f}'.format( item['Last'])), float('{:.10f}'.format(item['BaseVolume'])), \
             datetime.datetime.strptime(str(item['TimeStamp']), '%Y-%m-%dT%H:%M:%S.%f'), float('{:.10f}'.format( item['Bid'])),\
             float( '{:.10f}'.format(item['Ask'])), str(item['OpenBuyOrders']), str(item['OpenSellOrders']), float('{:.10f}'.format(item['PrevDay']))

            bitObjOHLC = BittrexOHLC(PairName=marketname, High=high, Low=low, Last=last,
                                 Volume=volume, BaseVolume=basevolume,
                                 TimeStamp=timestamp, Bid=bid, Ask=ask, OpenBuyOrders=openbuyorders,
                                 OpenSellOrders=opensellorders, PrevDay=prevday)
            bitObjOHLC.save()


def api_get_getticker(Pairs):
    if Pairs == '':
        Pairs == 'BTC-1ST'  #Доделал под текущую вьюху
    apiRequest = requests.get("https://bittrex.com/api/v1.1/public/" + "getticker?market="+Pairs)
    json_data = json.loads(apiRequest.text)
    if json_data['success']:
        root = json_data['result']
        bid, ask, last = float(root['Bid']), float(root['Ask']), str(root['Last'])
        bitObjTick = BittrexTick(PairName=Pairs, Tick=((ask + bid) / 2))
        bitObjTick.save()

