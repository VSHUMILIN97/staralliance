# https://www.binance.com/api/v3/ticker/bookTicker
import json
import logging
import requests
import asyncio
import redis
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../djangopiper'))
from PiedPiper.settings import REDIS_STARALLIANS_HOST, REDIS_DEFAULT_PORT

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename='/var/log/cryptopiper/binanceAPI.log')
#
conn_r = redis.ConnectionPool(host=REDIS_STARALLIANS_HOST, port=REDIS_DEFAULT_PORT, db=0)
r = redis.Redis(connection_pool=conn_r)
#
coins = \
    ['ADX', 'ETH', 'BTC', 'LTC', 'DASH', 'XRP', '1ST', '123', 'POE', 'MANA', 'LSK', 'EVX', 'ICN', 'QAX', 'XVG', 'SNM',
         'IOTA', 'NEO', 'MTL', 'YOYO', 'BNB', 'BCC', 'ZEC', 'BTG', 'REQ', 'ADA', 'AE', 'AION', 'AMB', 'APPC', 'ARK',
         'ARN', 'AST', 'AVT', 'BAT', 'BCD', 'BCH', 'BCP', 'BCPT', 'BLZ', 'BNT', 'BQX', 'BRD', 'BTS', 'CDT', 'CHAT',
         'CMT', 'CND', 'CTR', 'DAI', 'DGD', 'DLT', 'DNT', 'EDO', 'ELF', 'ENG', 'ENJ', 'EOS', 'ETC', 'FLI', 'FUEL',
         'FUN', 'GAS', 'GAT', 'GTO', 'GUP', 'GVT', 'GXS', 'HGT', 'HSR', 'ICX', 'IFT', 'IND', 'INS', 'IOST', 'KEY',
         'KMD', 'KNC', 'LEND', 'LEV', 'LINK', 'LOC', 'LRC', 'LUN', 'MAN', 'MCO', 'MDA', 'MGO', 'MKR', 'MOD', 'MTH',
         'NANO', 'NAV', 'NEBL', 'NULS', 'OAX', 'OMG', 'OST', 'PIVX', 'PIX', 'POWR', 'PPT', 'QSP', 'QTUM', 'RCN', 'RDN',
         'REP', 'RLC', 'RPX', 'SALT', 'SLT', 'SNGLS', 'SNT', 'STEEM', 'STORJ', 'STRAT', 'SUB', 'TNB', 'TNT', 'TRA',
         'TRIG', 'TRX', 'VEN', 'VIA', 'VIB', 'WABI', 'WAVES', 'WGS', 'WINGS', 'WTC', 'XLM', 'XMR', 'XZC', 'ZRX', 'GNO',
        'USDT', 'MLN', 'XBT', 'XDG', 'RRT', 'DSH', 'IOT', 'SAN', 'ETP', 'QTM', 'DAT', 'QSH', 'YYW', 'GNT', 'MNA', 'SPK',
     'AID', 'SNG']


def pair_fix(pair_string):
    for i in range(0, len(coins)):
        if str(pair_string).startswith(coins[i]) is True:
            test = pair_string.replace(coins[i], coins[i] + '-').split('-')
            pair_string = test[1] + '-' + test[0]
            return pair_string
        elif str(pair_string).startswith(coins[i]) is False:
            if i+1 < len(coins):
                continue
            else:
                return pair_string


async def binance_ticker():
    global api_request
    import os
    file_name = os.path.basename(sys.argv[0]).replace('.py', '')
    logging.info(u'Binance getticker started')
    #
    while 1:
        try:
            try:
                api_request = requests.get("https://www.binance.com/api/" + "v3/ticker/bookTicker")
            except ConnectionError:
                logging.error(u'Binance API cannot be reached')
            # Формируем JSON массив из данных с API
            if api_request.status_code == 200:
                json_data = json.loads(api_request.text)
                # Если все ок - парсим
                for item in json_data:
                    main_key = file_name + '/Binance/' + pair_fix(item['symbol'])
                    if r.get(main_key) is None:
                        r.set(main_key, 1)
                    if float(r.get(file_name + '/Binance/' +
                                   pair_fix(item['symbol'])).decode('utf-8')) != (float(item['bidPrice']) +
                                                                                  float(item['askPrice']))/2:
                        r.set(file_name + '/Binance/' + pair_fix(item['symbol']),
                              (float(item['bidPrice']) + float(item['askPrice'])) / 2)
                        r.publish('s-Binance', file_name + '/Binance/' + pair_fix(item['symbol']))
                        await asyncio.sleep(21/280)
                    else:
                        await asyncio.sleep(21/280)
                        continue
            #
        except OSError:
            logging.error(u'Binance parse mistake')
            continue


loop = asyncio.get_event_loop()
loop.run_until_complete(binance_ticker())
loop.run_forever()
