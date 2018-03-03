import asyncio
import json
import logging
import requests
from Exchanges.data_model import ExchangeModel

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


def pair_fix(pair_string):
    fixer = pair_string.split('/')
    pair_string = fixer[1] + '-' + fixer[0]
    return pair_string


async def livecoin_ticker():
    global api_request
    logging.info(u'livecoin getticker started')
    #
    while 1:
        try:
            #
            logging.info(u'Livecoin getticker API was called')
            try:
                api_request = requests.get("https://api.livecoin.net" + "/exchange/ticker")
            except ConnectionError:
                logging.error(u'Livecoin API cannot be reached')
            if api_request.status_code == 200:
                json_data = json.loads(api_request.text)
                for item in json_data:
                    ExchangeModel("LiveCoin", pair_fix(item['symbol']), float(item['best_bid']), float(item['best_ask']))
            await asyncio.sleep(18.4)
        except OSError:
            logging.error(u'Livecoin parse crash')
            continue


loop = asyncio.get_event_loop()
loop.run_until_complete(livecoin_ticker())
loop.run_forever()