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
  """
import json
from Exchanges.data_model import ExchangeModel
import requests
import logging

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


def bitfinex_ticker():
    global info_request, data_request
    logging.info('Bitfinex API method started')
    try:
        proxies = {'http': '47.89.41.164:80',
                   'https': '180.173.151.17:9797'}
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
            ExchangeModel('Bitfinex', pair_fix(items[0]), float(items[1]), float(items[3]))
    except OSError:
        logging.error('Bitfinex API crashed')
