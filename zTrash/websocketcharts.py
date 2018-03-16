import asyncio
import json
import logging
import websockets
from mongo_db_connection import MongoDBConnection

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


# Function, that provides connect between client and server.
# Works with async to prevent interrupting main thread.
async def echo(websocket, path):
    # After the connect with client was established open connect to MongoDB
    b = MongoDBConnection().start_local()
    db = b.PiedPiperStock
    # Checking for message from client. Trying to find what did he chose.
    async for message in websocket:
        # Parsing the string and setting Exchange name and Pair name
        exch = str(message).split('/')[2]
        pair = str(message).split('/')[3]
        while 1:
            tick = db[exch + 'Tick'].find({'PairName': pair, 'Aggregated': True})
            OHLC = db[exch].find({'PairName': pair, 'Aggregated': True})
            MHistSell = db[exch + 'MHist'].find({'PairName': pair, 'OrderType': 'SELL', 'Aggregated': True})
            MHistBuy = db[exch + 'MHist'].find({'PairName': pair, 'OrderType': 'BUY', 'Aggregated': True})
            # Importing library to transform data to JSON format
            from bson.json_util import dumps as dss
            ws_charts = {'tick': dss(tick), 'exchange': exch, 'pair': pair, 'ohlc': dss(OHLC), 'hsell': dss(MHistSell),
                         'hbuy': dss(MHistBuy)}
            ws_charts = json.dumps(ws_charts)
            # Creating a co-routine for pass data
            await websocket.send(ws_charts)
            # Closing the cursors
            try:
                tick.close()
                OHLC.close()
                MHistBuy.close()
                MHistSell.close()
            except():
                logging.error(u'No cursors to close at WSCharts')
            # Creating a co-routine. Sending a subprocess to sleep.
            await asyncio.sleep(40)


logging.info(u'Charts websocket started')
# Initialise websocket connection on host 127.0.0.1 and port 8070
asyncio.get_event_loop().run_until_complete(websockets.serve(echo, '127.0.0.1', 8070))
asyncio.get_event_loop().run_forever()
