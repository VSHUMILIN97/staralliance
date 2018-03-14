"""
[
  // on trading pairs (ex. tBTCUSD)
  [
    SYMBOL,
    BID,
    BID_SIZE,
    ASK,
    ASK_SIZE,
    DAILY_CHANGE,
    DAILY_CHANGE_PERC,
    LAST_PRICE,
    VOLUME,
    HIGH,
    LOW
  ]


  НА ЭТОЙ БИРЖЕ:
  1)КАПЧА
  2)ДОСТУП ТОЛЬКО ИЗ КИТАЯ
  3)ВРЕМЕННОЙ БЛОК
  """
import asyncio
import json
import requests
import logging
import redis
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../djangopiper'))
from PiedPiper.settings import REDIS_STARALLIANS_HOST, REDIS_DEFAULT_PORT

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename='/var/log/cryptopiper/bitfinexAPI.log')
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
    pair_string = pair_string.replace('t', '')
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


async def bitfinex_ticker():
    global info_request, data_request
    import os
    file_name = os.path.basename(sys.argv[0]).replace('.py', '')
    logging.info('Bitfinex API method started')
    while 1:
        try:
            proxies = {'http': '219.223.251.173:3128',
                       'https': '219.223.251.173:3128'}
            try:
                info_request = requests.get("https://api.bitfinex.com/v1/symbols", proxies=proxies, timeout=5)
            except ConnectionError:
                logging.error(u'Bitfinex info API cannot be reached')
            info_data = json.loads(info_request.text)
            pair_string = ''
            for name in range(0, len(info_data)):
                pair_string += 't' + info_data[name].upper()
                if name + 1 < len(info_data):
                    pair_string += ','
            try:
                data_request = requests.get("https://api.bitfinex.com/v2/tickers?symbols=" + pair_string,
                                            proxies=proxies, timeout=5)
            except ConnectionError:
                logging.error(u'Bitfinex API cannot be reached')
            full_data = json.loads(data_request.text)
            for items in full_data:
                main_key = file_name + '/Bitfinex/' + pair_fix(items[0])
                if r.get(main_key) is None:
                    r.set(main_key, 1)
                r.set(file_name + '/Bitfinex/' + pair_fix(items[0]), (float(items[1]) + float(items[3]))/2)
                if float(r.get(file_name + '/Bitfinex/' +
                               pair_fix(items[0])).decode('utf-8')) != (float(items[1]) + float(items[3]))/2:
                    r.set(file_name + '/Bitfinex/' + pair_fix(items[0]), (float(items[1]) + float(items[3])) / 2)
                    r.publish('s-Bitfinex', file_name + '/Bitfinex/' + pair_fix(items[0]))
                else:
                    continue
            await asyncio.sleep(32)
        except OSError:
            logging.error('Bitfinex API crashed')
            continue


loop = asyncio.get_event_loop()
loop.run_until_complete(bitfinex_ticker())
loop.run_forever()