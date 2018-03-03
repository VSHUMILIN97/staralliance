# https://poloniex.com/public?command=returnTicker
import asyncio
import json
import logging
import requests
from Exchanges.data_model import ExchangeModel

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

pairlist = ['BTC_ETH', 'BTC_LTC', 'BTC_DASH', 'BTC_XRP']


def pair_fix(pair_string):
    return str(pair_string).replace('_', '-')


async def poloniex_ticker():
    global api_request
    logging.info(u'Poloniex getticker started')
    while 1:
        #
        try:
            api_request = requests.get("https://poloniex.com/public" + "?command=returnTicker")
        except ConnectionError:
            logging.error(u'Poloniex API cannot be reached')
        #
        if api_request.status_code == 200:
            json_data = json.loads(api_request.text)
            for item in json_data:
                ExchangeModel("Poloniex", pair_fix(item), float(json_data[item]['highestBid']),
                              float(json_data[item]['lowestAsk']))
        await asyncio.sleep(16.9)


loop = asyncio.get_event_loop()
loop.run_until_complete(poloniex_ticker())
loop.run_forever()