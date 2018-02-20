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


def kraken_ticker():
    global eu_name_index
    logging.info('Kraken API has started')
    try:
        info_request = requests.get("https://api.kraken.com/0/public/AssetPairs")
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
        data_request = requests.get("https://api.kraken.com/0/public/Ticker?pair=" + pair_string)
        json_data = json.loads(data_request.text)
        data = json_data['result']
        iterable2 = 0
        for each_item in data:
            data_alt_var = data[each_item]
            if each_item in alt_china_name:
                eu_name_index = alt_china_name.index(each_item)
            ExchangeModel('Kraken', pair_fix(alt_name[eu_name_index]), float(data_alt_var['b'][0]), float(data_alt_var['a'][0]))
            iterable2 += 1
        logging.info('Kraken API executed')
    except():
        logging.error('Kraken API was prevented from execution')
