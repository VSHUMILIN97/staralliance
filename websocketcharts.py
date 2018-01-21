import asyncio
import datetime
import json
import logging
import websockets
import Exchanges.TimeAggregator
from mongo_db_connection import MongoDBConnection

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


async def echo(websocket, path):
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    async for message in websocket:
        exch = str(message).split('/')[2]
        pair = str(message).split('/')[3]
        while 1:
            tick = db[exch + 'Tick'].find({'PairName': pair, 'Aggregated': True})
            OHLC = db.Bittrex.find({'PairName': pair, 'Aggregated': True})
            MHistSell = db.BittrexMHist.find({'PairName': pair, 'OrderType': 'SELL', 'Aggregated': True})
            MHistBuy = db.BittrexMHist.find({'PairName': pair, 'OrderType': 'BUY', 'Aggregated': True})
            from bson.json_util import dumps as dss
            ws_charts = {'tick': dss(tick), 'exchange': exch, 'pair': pair, 'ohlc': dss(OHLC), 'hsell': dss(MHistSell),
                         'hbuy': dss(MHistBuy)}
            ws_charts = json.dumps(ws_charts)
            await websocket.send(ws_charts)
            await asyncio.sleep(40)


logging.info(u'Charts websocket started')
asyncio.get_event_loop().run_until_complete(websockets.serve(echo, '127.0.0.1', 8070))
asyncio.get_event_loop().run_forever()
