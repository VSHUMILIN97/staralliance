# https://api.gatecoin.com/Public/LiveTickers
import asyncio
import json
import logging
import requests
import redis
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../cryptopiper'))
from PiedPiper.settings import REDIS_STARALLIANS_HOST, REDIS_DEFAULT_PORT

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename='/var/log/cryptopiper/gatecoinAPI.log')
conn_r = redis.ConnectionPool(host=REDIS_STARALLIANS_HOST, port=REDIS_DEFAULT_PORT, db=0)
r = redis.Redis(connection_pool=conn_r)


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


async def gatecoin_ticker():
    global api_request
    import os
    file_name = os.path.basename(sys.argv[0]).replace('.py', '')
    logging.info(u'Gatecoin collection of data in parse')
    while 1:
        try:
            try:
                api_request = requests.get("https://api.gatecoin.com/Public/LiveTickers")
            except ConnectionError:
                logging.error(u'Gatecoin API cannot be reached')
            #
            if api_request.status_code == 200:
                json_data = json.loads(api_request.text)
                result = json_data['tickers']
                for item in result:
                    main_key = file_name + '/Gatecoin/' + pair_fix(item['currencyPair'])
                    if r.get(main_key) is None:
                        r.set(main_key, 1)
                    if float(r.get(file_name + '/Gatecoin/' +
                                   pair_fix(item['currencyPair'])).decode('utf-8')) != (float(item['bid'])
                                                                                        + float(item['ask']))/2:
                        r.set(file_name + '/Gatecoin/' + pair_fix(item['currencyPair']),
                              (float(item['bid']) + float(item['ask'])) / 2)
                        r.publish('s-Gatecoin', file_name + '/Gatecoin/' + pair_fix(item['currencyPair']))
                        await asyncio.sleep(19.7/72)
                    else:
                        await asyncio.sleep(19.7/72)
                        continue
        #
        except OSError:
            logging.error(r'Gatecoin ticker mistake')
            continue


loop = asyncio.get_event_loop()
loop.run_until_complete(gatecoin_ticker())
loop.run_forever()
