# https://api.kucoin.com/v1/open/tick
import asyncio
import json
import logging
import requests
import redis
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../cryptopiper'))
from PiedPiper.settings import STARALLIANS_HOST, REDIS_DEFAULT_PORT

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename='/var/log/cryptopiper/kucoinAPI.log')
conn_r = redis.ConnectionPool(host=STARALLIANS_HOST, port=REDIS_DEFAULT_PORT, db=0)
r = redis.Redis(connection_pool=conn_r)


def pair_fix(pair_string):
    fixer = pair_string.split('-')
    pair_string = fixer[1] + '-' + fixer[0]
    return pair_string


async def kucoin_ticker():
    # Данные собираются для каждой валютной пары из списка pairlist
    global info_request
    import os
    file_name = os.path.basename(sys.argv[0]).replace('.py', '')
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
                        main_key = file_name + '/Kucoin/' + pair_fix(item['symbol'])
                        if r.get(main_key) is None:
                            r.set(main_key, 1)
                        if float(r.get(file_name + '/Kucoin/'
                                 + pair_fix(item['symbol'])).decode('utf-8')) != (float(item['buy'])
                                                                                  + float(item['sell']))/2:
                            r.set(file_name + '/Kucoin/' + pair_fix(item['symbol']),
                                  (float(item['buy']) + float(item['sell'])) / 2)
                            r.publish('s-Kucoin', file_name + '/Kucoin/' + pair_fix(item['symbol']))
                            await asyncio.sleep(16 / 298)
                        else:
                            await asyncio.sleep(16 / 298)
                            continue
                    except KeyError:
                        continue
                    except AttributeError:
                        continue
        #
        except OSError:
            logging.info(u'Kucoin parse crash')
            continue


loop = asyncio.get_event_loop()
loop.run_until_complete(kucoin_ticker())
loop.run_forever()
