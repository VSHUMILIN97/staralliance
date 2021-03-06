# https://bleutrade.com/api/v2/public/getticker?market=ETH_BTC,LTC_BTC
import json
import logging
import asyncio
import requests
import redis
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../cryptopiper'))
from PiedPiper.settings import STARALLIANS_HOST, REDIS_DEFAULT_PORT

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename='/var/log/cryptopiper/bleutradeAPI.log')

conn_r = redis.ConnectionPool(host=STARALLIANS_HOST, port=REDIS_DEFAULT_PORT, db=0)
r = redis.Redis(connection_pool=conn_r)


def pair_fix(pair_string):
    fixer = pair_string.split('_')
    pair_string = fixer[1] + '-' + fixer[0]
    return pair_string


async def bleutrade_ticker():
    # Данные собираются для каждой валютной пары из списка pairlist
    global info_request, api_request
    import os
    file_name = os.path.basename(sys.argv[0]).replace('.py', '')
    logging.info(u'Bleutrade getticker started')
    while 1:
        try:
            try:
                info_request = requests.get("https://bleutrade.com/api/v2/public/getmarkets")
            except ConnectionError:
                logging.error(u'Bleutrade info API cannot be reached')
            info_data = json.loads(info_request.text)
            data = info_data['result']
            pair_string = ""
            for each_index in range(0, len(data)):
                pair_string += data[each_index]['MarketName']
                if each_index + 1 != len(data):
                    pair_string += ","
            try:
                api_request = requests.get("https://bleutrade.com/api/v2/public/" + "getticker?market=" + pair_string)
            except ConnectionError:
                logging.error(u'Bleutrade API cannot be reached')
            # Формируем JSON массив из данных с API. Проверяем код ответа.
            pair_array = pair_string.split(',')
            if api_request.status_code == 200:
                json_data = json.loads(api_request.text)
                # Если все ок - парсим
                # Назначаем объект 'result' корневым, для простоты обращения
                root = json_data['result']
                index = 0
                for item in root:
                    main_key = file_name + '/Bleutrade/' + pair_fix(pair_array[index])
                    if r.get(main_key) is None:
                        r.set(main_key, 1)
                    if float(r.get(file_name + '/Bleutrade/' +
                                   pair_fix(pair_array[index])).decode('utf-8')) != (float(item['Bid']) +
                                                                                     float(item['Ask']))/2:
                        r.set(file_name + '/Bleutrade/' + pair_fix(pair_array[index]),
                              (float(item['Bid']) + float(item['Ask'])) / 2)
                        r.publish('s-Bleutrade', file_name + '/Bleutrade/' + pair_fix(pair_array[index]))
                        await asyncio.sleep(13.8 / 138)

                    else:
                        await asyncio.sleep(13.8 / 138)
                        continue
                    index += 1
        #
        except OSError:
            logging.info(u'Bleutrade parse mistake')
            continue


loop = asyncio.get_event_loop()
loop.run_until_complete(bleutrade_ticker())
loop.run_forever()
