# https://poloniex.com/public?command=returnTicker
import asyncio
import json
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../cryptopiper'))
import logging
import requests
import redis
from PiedPiper.settings import STARALLIANS_HOST, REDIS_DEFAULT_PORT

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename='/var/log/cryptopiper/poloniexAPI.log')

conn_r = redis.ConnectionPool(host=STARALLIANS_HOST, port=REDIS_DEFAULT_PORT, db=0)
r = redis.Redis(connection_pool=conn_r)


def pair_fix(pair_string):
    return str(pair_string).replace('_', '-')


async def poloniex_ticker():
    global api_request
    import os
    file_name = os.path.basename(sys.argv[0]).replace('.py', '')
    logging.info(u'Poloniex getticker started')
    while 1:
        #
        try:
            try:
                api_request = requests.get("https://poloniex.com/public" + "?command=returnTicker")
            except ConnectionError:
                logging.error(u'Poloniex API cannot be reached')
            #
            if api_request.status_code == 200:
                json_data = json.loads(api_request.text)
                for item in json_data:
                    main_key = file_name + '/Poloniex/' + pair_fix(item)
                    if r.get(main_key) is None:
                        r.set(main_key, 1)
                    if float(r.get(main_key).decode('utf-8')) != (float(json_data[item]['highestBid']) +
                                                                  float(json_data[item]['lowestAsk']))/2:
                        r.set(main_key, (float(json_data[item]['highestBid']) + float(json_data[item]['lowestAsk']))/2)
                        r.publish('s-Poloniex', main_key)
                        await asyncio.sleep(17/99)
                    else:
                        await asyncio.sleep(17/99)
                        continue
        except OSError:
            logging.info('NO INTERNET CONNECTION')
            continue

loop = asyncio.get_event_loop()
loop.run_until_complete(poloniex_ticker())
loop.run_forever()
