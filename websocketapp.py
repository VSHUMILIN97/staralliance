import asyncio
import time
import json
import logging
import redis
import websockets


from Exchanges.ExchangeAPI.PairDataNOTAPI import approved_keys
from PiedPiper.settings import STARALLIANS_HOST, REDIS_DEFAULT_PORT, LOCAL_SERVICE_HOST

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename='/var/log/cryptopiper/websockets.log')

# Function, that provides connect between client and server.
# Works with async to prevent interrupting main thread.
async def arbitration_socket(websocket, path):
    # After the connect with client was established open connect to MongoDB
    conn_r = redis.ConnectionPool(host=LOCAL_SERVICE_HOST, port=REDIS_DEFAULT_PORT, db=0)
    r = redis.Redis(connection_pool=conn_r)
    p = r.pubsub()
    p.psubscribe('s-*')
    all_the_current_keys = approved_keys()
    while True:
        message = p.get_message()
        if message:
            try:
                try:
                    logging.info(dict(message)['data'].decode('utf-8'))
                    msg = dict(message)['data'].decode('utf-8')
                except AttributeError:
                    continue
                if msg in all_the_current_keys:
                    await websocket.send(json.dumps([msg.split('/')[1] + '/'
                                                    + msg.split('/')[2],
                                                    r.get(msg).decode('utf-8')]))
            except TypeError:
                pass
        await websocket.send(r.get('poloniexAPI/Poloniex/BTC-LBC').decode('utf-8'))
        time.sleep(0.001)


logging.info(u'Arbitartion websocket started')
# Initialise websocket connection on host 0.0.0.0 and port 8091
asyncio.get_event_loop().run_until_complete(websockets.serve(arbitration_socket, '0.0.0.0', 8091))
asyncio.get_event_loop().run_forever()


