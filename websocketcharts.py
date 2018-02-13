import asyncio
import json
import logging
import websockets
from mongo_db_connection import MongoDBConnection

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.WARNING, filename='/var/log/cryptopiper/charts_WS.log')


async def echo(websocket, path):
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    async for message in websocket:
        exch = str(message).split('/')[2]
        pair = str(message).split('/')[3]
        while 1:
            tick = db[exch + 'Tick'].find({'PairName': pair, 'Aggregated': True})
            OHLC = db[exch].find({'PairName': pair, 'Aggregated': True})
            MHistSell = db[exch + 'MHist'].find({'PairName': pair, 'OrderType': 'SELL', 'Aggregated': True})
            MHistBuy = db[exch + 'MHist'].find({'PairName': pair, 'OrderType': 'BUY', 'Aggregated': True})
            from bson.json_util import dumps as dss
            ws_charts = {'tick': dss(tick), 'exchange': exch, 'pair': pair, 'ohlc': dss(OHLC), 'hsell': dss(MHistSell),
                         'hbuy': dss(MHistBuy)}
            ws_charts = json.dumps(ws_charts)
            await websocket.send(ws_charts)
            try:
                tick.close()
                OHLC.close()
                MHistBuy.close()
                MHistSell.close()
            except():
                logging.error(u'No cursors to close at WSCharts')
            await asyncio.sleep(40)


logging.info(u'Charts websocket started')
asyncio.get_event_loop().run_until_complete(websockets.serve(echo, '127.0.0.1', 8070))
asyncio.get_event_loop().run_forever()
