import asyncio
import json
import logging
import requests
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../cryptopiper'))
from mongo_db_connection import MongoDBConnection

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename='/var/log/cryptopiper/coinmarketcapAPI.log')

async def main_page_parser():
    target_coins = ['BTC', 'ETH', 'LTC', 'DASH', 'XMR', 'XRP']
    b = MongoDBConnection().start_local()
    db = b.PiedPiperStock
    test = db.MainPage
    while 1:
        try:
            coin_stack = []
            try:
                api_request = requests.get("https://api.coinmarketcap.com/v1/ticker/")
            except ConnectionError:
                logging.error(u'coinmarketcapAPI cannot be reached')
            #
            if api_request.status_code == 200:
                json_data = json.loads(api_request.text)
                for item in json_data:
                    if item['symbol'] in target_coins:
                        coin_stack.append({item['symbol']: item['price_usd']})
                test.drop()
                test.insert(coin_stack)
            else:
                pass
            await asyncio.sleep(20)
        except OSError:
            logging.error('No internet connection on CMCAPI!')


loop = asyncio.get_event_loop()
loop.run_until_complete(main_page_parser())
loop.run_forever()
