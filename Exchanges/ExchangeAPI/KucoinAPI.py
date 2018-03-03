# https://api.kucoin.com/v1/open/tick
import asyncio
import json
import logging
import requests
from Exchanges.data_model import ExchangeModel


def pair_fix(pair_string):
    fixer = pair_string.split('-')
    pair_string = fixer[1] + '-' + fixer[0]
    return pair_string


async def kucoin_ticker():
    # Данные собираются для каждой валютной пары из списка pairlist
    global info_request
    logging.info(u'Kucoin getticker started')
    while 1:
        try:
            try:
                info_request = requests.get("https://api.kucoin.com/v1/open/tick")
            except ConnectionError:
                logging.error(u'Kucoin API cannot be reached')
            info_data = json.loads(info_request.text)
            if info_data['code'] == 'OK':
                data = info_data['data']
                for item in data:
                    try:
                        ExchangeModel('Kucoin', pair_fix(item['symbol']), float(item['buy']), float(item['sell']))
                    except KeyError:
                        continue
            await asyncio.sleep(14.9)
        except OSError:
            logging.info(u'Kucoin parse crash')
            continue


loop = asyncio.get_event_loop()
loop.run_until_complete(kucoin_ticker())
loop.run_forever()
