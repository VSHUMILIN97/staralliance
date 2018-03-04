import asyncio
import json
import logging
import redis
import requests
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../djangopiper'))
from PiedPiper.settings import REDIS_HOST, REDIS_PORT


logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)
r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def pair_fix(pair_string):
    fixer = pair_string.split('/')
    pair_string = fixer[1] + '-' + fixer[0]
    return pair_string


async def livecoin_ticker():
    global api_request
    logging.info(u'livecoin getticker started')
    #
    import os
    file_name = os.path.basename(sys.argv[0])
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
                    if float(r.get(file_name + '/Livecoin/' +
                             pair_fix(item['symbol'])).decode('utf-8')) != (float(item['best_bid'])
                                                                            + float(item['best_ask']))/2:
                        r.set(file_name + '/Livecoin/' + pair_fix(item['symbol']),
                              (float(item['best_bid']) + float(item['best_ask']))/2)
                    else:
                        continue
            await asyncio.sleep(18.4)
        except OSError:
            logging.error(u'Livecoin parse crash')
            continue


loop = asyncio.get_event_loop()
loop.run_until_complete(livecoin_ticker())
loop.run_forever()
