# https://api.liqui.io/api/3/depth/eth_btc-ltc_btc?limit=1&ignore_invalid=1
import asyncio
import json
import logging
import requests
from Exchanges.data_model import ExchangeModel

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


def pair_fix(pair_string):
    fixer = pair_string.split('_')
    pair_string = fixer[1] + '-' + fixer[0]
    return str(pair_string.upper())


async def liqui_ticker():
    global best_ask, best_bid, info_request, api_request
    logging.info(u'Liqui getticker started')
    #
    while 1:
        try:
            try:
                info_request = requests.get("https://api.liqui.io/api/3/info")
            except ConnectionError:
                logging.error(u'Liqui info API cannot be reached')
            info_data = json.loads(info_request.text)
            pairs = info_data['pairs']
            pair_string = ""
            for each in pairs:
                pair_string += each + '-'
            try:
                api_request = requests.get("https://api.liqui.io" + "/api/3/ticker/" + pair_string +
                                           '?limit=1&ignore_invalid=1')
            except ConnectionError:
                logging.error(u'Liqui API cannot be reached')
            # Формируем JSON массив из данных с API
            if api_request.status_code == 200:
                json_data = json.loads(api_request.text)
                # Если все ок - парсим
                try:
                    for item in json_data:
                        ExchangeModel("Liqui", pair_fix(item), json_data[item]['buy'], json_data[item]['sell'])
                except LookupError:
                    logging.critical(u'Liqui API returned 0 elements')
            await asyncio.sleep(21.12)
        except OSError:
            logging.error(u'Liqui parse mistake')
            continue


loop = asyncio.get_event_loop()
loop.run_until_complete(liqui_ticker())
loop.run_forever()
