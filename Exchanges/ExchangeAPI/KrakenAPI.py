import asyncio
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../cryptopiper'))
import json
import redis
import requests
import logging
from PiedPiper.settings import REDIS_STARALLIANS_HOST, REDIS_DEFAULT_PORT

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename='/var/log/cryptopiper/krakenAPI.log')
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


async def kraken_ticker():
    global eu_name_index, info_request, data_request
    import os
    file_name = os.path.basename(sys.argv[0]).replace('.py', '')
    logging.info('Kraken API has started')
    while 1:
        try:
            try:
                info_request = requests.get("https://api.kraken.com/0/public/AssetPairs")
            except ConnectionError:
                logging.error(u'Kraken info API cannot be reached')
            info_data = json.loads(info_request.text)
            info_name = info_data['result']
            pair_string = ''
            china_string = ''
            iterable1 = 0
            for name in info_name:
                name_alt_var = info_name[name]
                china_string += name
                pair_string += name_alt_var['altname']
                if iterable1 + 1 < len(info_name):
                    pair_string += ','
                    china_string += ','
                iterable1 += 1
            #
            alt_name = pair_string.split(',')
            alt_china_name = china_string.split(',')
            try:
                data_request = requests.get("https://api.kraken.com/0/public/Ticker?pair=" + pair_string)
            except ConnectionError:
                logging.error(u'Kraken API cannot be reached')
            json_data = json.loads(data_request.text)
            data = json_data['result']
            for each_item in data:
                data_alt_var = data[each_item]
                if each_item in alt_china_name:
                    eu_name_index = alt_china_name.index(each_item)
                main_key = file_name + '/Kraken/' + pair_fix(alt_name[eu_name_index])
                if r.get(main_key) is None:
                    r.set(main_key, 1)
                if float(r.get(file_name + '/Kraken/' +
                               pair_fix(alt_name[eu_name_index])).decode('utf-8')) != (float(data_alt_var['b'][0]) +
                                                                                       float(data_alt_var['a'][0]))/2:
                    r.set(file_name + '/Kraken/' + pair_fix(alt_name[eu_name_index]),
                          (float(data_alt_var['b'][0]) + float(data_alt_var['a'][0])) / 2)
                    r.publish('s-Kraken', file_name + '/Kraken/' + pair_fix(alt_name[eu_name_index]))
                    await asyncio.sleep(24/57)
                else:
                    await asyncio.sleep(24/57)
                    continue
        #
        except OSError:
            logging.error('Kraken API was prevented from execution')
            continue


loop = asyncio.get_event_loop()
loop.run_until_complete(kraken_ticker())
loop.run_forever()
