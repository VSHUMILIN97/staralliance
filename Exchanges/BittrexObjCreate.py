import requests
import json
import time
from Exchanges.views import Bittrex


def api_get_getmarketsummaries():
    print('Before Bittrix call attempt to server - ' + str(time.time()))
    apiRequest = requests.get("https://bittrex.com/api/v1.1/public/" + "getmarketsummaries")
    json_data = json.loads(apiRequest.text)
    print("api get.Bittrix is called - " + str(time.time()))
    if json_data['success']:
        result = json_data['result']
        for item in result:
            marketname, high, low, volume, last, basevolume, timestamp, bid, ask, openbuyorders, opensellorders, prevday = str(
                item['MarketName']), \
                                                                                                                           float(
                                                                                                                               '{:.10f}'.format(
                                                                                                                                   item[
                                                                                                                                       'High'])), \
                                                                                                                           float(
                                                                                                                               '{:.10f}'.format(
                                                                                                                                   item[
                                                                                                                                       'Low'])), \
                                                                                                                           float(
                                                                                                                               '{:.10f}'.format(
                                                                                                                                   item[
                                                                                                                                       'Last'])), float(
                '{:.10f}'.format(item['Volume'])), \
                                                                                                                           float(
                                                                                                                               '{:.10f}'.format(item[
                                                                                                                                   'BaseVolume'])), str(
                item['TimeStamp']), \
                                                                                                                           float(
                                                                                                                               '{:.10f}'.format(
                                                                                                                                   item[
                                                                                                                                       'Bid'])), float(
                '{:.10f}'.format(item['Ask'])), \
                                                                                                                           str(
                                                                                                                               item[
                                                                                                                                   'OpenBuyOrders']), str(
                item['OpenSellOrders']), \
                                                                                                                           float(
                                                                                                                               '{:.10f}'.format(
                                                                                                                                   item[
                                                                                                                                       'PrevDay']))

            bitObj = Bittrex(PairName = marketname, High = high
                             , Low = low, Volume = volume,
                             Last = last, BaseVolume = basevolume,
                             TimeStamp = timestamp, Bid = bid, Ask = ask, OpenBuyOrders = openbuyorders,
                             OpenSellOrders = opensellorders,
                             PrevDay = prevday)
            bitObj.save()

