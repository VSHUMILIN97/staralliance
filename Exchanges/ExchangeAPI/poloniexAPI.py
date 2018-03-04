# https://poloniex.com/public?command=returnTicker
import asyncio
import json
import logging
import requests
import redis
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../djangopiper'))
from PiedPiper.settings import REDIS_HOST, REDIS_PORT

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)
r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def pair_fix(pair_string):
    return str(pair_string).replace('_', '-')


async def poloniex_ticker():
    global api_request
    import os
    file_name = os.path.basename(sys.argv[0])
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
                if float(r.get(file_name+'/Poloniex/' + pair_fix(item)).decode('utf-8')) != (float(json_data[item]
                                                                                                   ['highestBid']) +
                                                                                             float(json_data[item]
                                                                                                   ['lowestAsk']))/2:
                    r.set(file_name + '/Poloniex/' + pair_fix(item), (float(json_data[item]['highestBid']) +
                          float(json_data[item]['lowestAsk']))/2)
                    r.publish('keychannel', file_name + '/Poloniex/' + pair_fix(item))
                else:
                    continue
        await asyncio.sleep(16.9)


loop = asyncio.get_event_loop()
loop.run_until_complete(poloniex_ticker())
loop.run_forever()