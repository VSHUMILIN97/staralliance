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
     'AID', 'SNG', 'USD']


def pair_fix(pair_string):
    pair_string = pair_string.replace('t', '')
    for i in range(0, len(coins)):
        if str(pair_string).endswith(coins[i]) is True:
            test = pair_string.replace(coins[i], '-' + coins[i]).split('-')
            pair_string = test[1] + '-' + test[0]
            return pair_string
        elif str(pair_string).startswith(coins[i]) is False:
            if i+1 < len(coins):
                continue
            else:
                return pair_string


async def hitbtc_ticker():
    global data_request
    import os
    file_name = os.path.basename(sys.argv[0]).replace('.py', '')
    logging.info("HitbtcAPI method started")
    while 1:
        try:
            try:
                data_request = requests.get("https://api.hitbtc.com/api/2/public/ticker")
            except ConnectionError:
                logging.error(u'HitBTC API cannot be reached')
            full_data = json.loads(data_request.text)
            for item in full_data:
                try:
                    main_key = file_name + '/Hitbtc/' + pair_fix(item['symbol'])
                    if r.get(main_key) is None:
                        r.set(main_key, 1)
                    if float(r.get(file_name + '/Hitbtc/' +
                                   pair_fix(item['symbol'])).decode('utf-8')) != (float(item['bid']) +
                                                                                  float(item['ask']))/2:
                        r.set(file_name + '/Hitbtc/' + pair_fix(item['symbol']),
                              (float(item['bid']) + float(item['ask'])) / 2)
                        r.publish('s-Hitbtc', file_name + '/Hitbtc/' + pair_fix(item['symbol']))
                    else:
                        continue
                except TypeError:
                    logging.info('null in data parsing at ' + pair_fix(item['symbol']))
                    continue
                except AttributeError:
                    logging.info('NoneType at redis DB, pair - ' + pair_fix(item['symbol']))
                    # Add if/else statement that'll check, whether pair is null now or not, if not it'll add it to redis
                    continue
            await asyncio.sleep(25.9)
        except OSError:
            logging.error('HitbtcAPI method crashed')
            continue


loop = asyncio.get_event_loop()
loop.run_until_complete(hitbtc_ticker())
loop.run_forever()
