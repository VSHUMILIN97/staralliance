# https://api.kucoin.com/v1/open/tick
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
    fixer = pair_string.split('-')
    pair_string = fixer[1] + '-' + fixer[0]
    return pair_string


async def kucoin_ticker():
    # Данные собираются для каждой валютной пары из списка pairlist
    global info_request
    import os
    file_name = os.path.basename(sys.argv[0])
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
                        if float(r.get(file_name + '/Kucoin/'
                                 + pair_fix(item['symbol'])).decode('utf-8')) != (float(item['buy'])
                                                                                  + float(item['sell']))/2:
                            r.set(file_name + '/Kucoin/' + pair_fix(item['symbol']),
                                  (float(item['buy']) + float(item['sell'])) / 2)
                            logging.info('There was a change')
                        else:
                            logging.info('There were no changes at ' + file_name + '/Kucoin/' + pair_fix(item['symbol']))
                            continue
                    except KeyError:
                        continue
                    except AttributeError:
                        continue
            await asyncio.sleep(14.9)
        except OSError:
            logging.info(u'Kucoin parse crash')
            continue


loop = asyncio.get_event_loop()
loop.run_until_complete(kucoin_ticker())
loop.run_forever()
