import asyncio
import time
import json
import logging
import redis
import websockets
from Exchanges.ExchangeAPI.PairDataNOTAPI import approved_keys
from PiedPiper.settings import REDIS_HOST, REDIS_PORT
from mongo_db_connection import MongoDBConnection


logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)
r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

p = r.pubsub()
p.subscribe('keychannel')


# Function, that provides connect between client and server.
# Works with async to prevent interrupting main thread.
async def arbitration_socket(websocket, path):
    # After the connect with client was established open connect to MongoDB
    all_the_current_keys = approved_keys()
    while 1:
        try:
            msg = bytes(dict(p.get_message())['data'])
        except TypeError:
            time.sleep(0.01)
            continue
        if msg.decode('utf-8') in all_the_current_keys:
            try:
                logging.info(msg.decode('utf-8') + ' ' + r.get(msg.decode('utf-8')).decode('utf-8'))
                await websocket.send(json.dumps({msg.decode('utf-8').split('/')[1] + '/'
                                                 + msg.decode('utf-8').split('/')[2]:
                                                 r.get(msg.decode('utf-8')).decode('utf-8')}))
            except AttributeError:
                time.sleep(0.001)

logging.info(u'Arbitartion websocket started')
# Initialise websocket connection on host 127.0.0.1 and port 8090
asyncio.get_event_loop().run_until_complete(websockets.serve(arbitration_socket, '127.0.0.1', 8090))
asyncio.get_event_loop().run_forever()



