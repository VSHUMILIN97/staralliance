import asyncio
import json
import logging
import redis
import requests
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../cryptopiper'))
from PiedPiper.settings import STARALLIANS_HOST, REDIS_DEFAULT_PORT


logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename='/var/log/cryptopiper/livecoinAPI.log')
conn_r = redis.ConnectionPool(host=STARALLIANS_HOST, port=REDIS_DEFAULT_PORT, db=0)
r = redis.Redis(connection_pool=conn_r)


def pair_fix(pair_string):
    fixer = pair_string.split('/')
    pair_string = fixer[1] + '-' + fixer[0]
    return pair_string


async def livecoin_ticker():
    global api_request
    logging.info(u'livecoin getticker started')
    #
    import os
    file_name = os.path.basename(sys.argv[0]).replace('.py', '')
    while 1:
        try:
            #
            logging.info(u'Livecoin getticker API was called')
            try:
                api_request = requests.get("https://api.livecoin.net" + "/exchange/ticker")
            except ConnectionError:
                logging.error(u'Livecoin API cannot be reached')
            j = 0
            if api_request.status_code == 200:
                json_data = json.loads(api_request.text)
                for item in json_data:
                    j += 1
                    main_key = file_name + '/Livecoin/' + pair_fix(item['symbol'])
                    if r.get(main_key) is None:
                        r.set(main_key, 1)
                    if float(r.get(file_name + '/Livecoin/' +
                             pair_fix(item['symbol'])).decode('utf-8')) != (float(item['best_bid'])
                                                                            + float(item['best_ask']))/2:
                        r.set(file_name + '/Livecoin/' + pair_fix(item['symbol']),
                              (float(item['best_bid']) + float(item['best_ask']))/2)
                        r.publish('s-Livecoin', file_name + '/Livecoin/' + pair_fix(item['symbol']))
                        await asyncio.sleep(26 / 520)
                    else:
                        await asyncio.sleep(26 / 520)
                        continue
        #
        except OSError:
            logging.error(u'Livecoin parse crash')
            continue


loop = asyncio.get_event_loop()
loop.run_until_complete(livecoin_ticker())
loop.run_forever()
