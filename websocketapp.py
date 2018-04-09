import asyncio
import ssl
from ssl import SSLContext
import threading
import time
import json
import logging
from _ssl import PROTOCOL_TLS

import aredis
import redis
import websockets


from Exchanges.ExchangeAPI.PairDataNOTAPI import approved_keys
from PiedPiper.settings import STARALLIANS_HOST, REDIS_DEFAULT_PORT, LOCAL_SERVICE_HOST

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)#, filename='/var/log/cryptopiper/websockets.log')

websockets_all = []

# NOT IN USE
# Function, that provides connect between client and server.
# Works with async to prevent interrupting main thread.
async def arbitration_socket(websocket, path):
    websockets_all.append(websocket)
    conn_r = redis.ConnectionPool(host=LOCAL_SERVICE_HOST, port=REDIS_DEFAULT_PORT, db=0)
    r = redis.Redis(connection_pool=conn_r)
    p = r.pubsub()
    p.psubscribe('s-*')
    # After the connect with client was established open connect to MongoDB
    all_the_current_keys = approved_keys()
    while True:
        message = p.get_message()
        if message:
            try:
                try:
                    msg = dict(message)['data'].decode('utf-8')
                except AttributeError:
                    continue
                if msg in all_the_current_keys:
                    for websocket in websockets_all:
                        await websocket.send(json.dumps([msg.split('/')[1] + '/'
                                                     + msg.split('/')[2], r.get(msg).decode('utf-8')]))
            except TypeError:
                pass
        time.sleep(0.001)


async def handler(websocket, path):
    websockets_all.append(websocket)
    r = aredis.StrictRedis(host=LOCAL_SERVICE_HOST, port=REDIS_DEFAULT_PORT, db=0)
    # r = redis.Redis(connection_pool=conn_r)
    p = r.pubsub()
    await p.psubscribe('s-*')
    # After the connect with client was established open connect to MongoDB
    all_the_current_keys = approved_keys()
    # Register.
    try:
        while True:
            message = await p.get_message()
            if message:
                msg = dict(message)['data']
                if msg == 1:
                    continue
                else:
                    msg = dict(message)['data'].decode('utf-8')
                    exch = str(msg.split('/')[1])
                    pair = str(msg.split('/')[2])
                    pretick = await r.get(msg)
                    tick = str(pretick.decode('utf-8'))
                if msg in all_the_current_keys:
                    await websocket.send(json.dumps([exch + '/' + pair, tick]))
                #else:
                  #  pass
    #
    finally:
        # Unregister.
        pass

ctx = ssl.create_default_context()
ctx.load_cert_chain('/etc/letsencrypt/live/staralliance.pro-0001/fullchain.pem',
                    '/etc/letsencrypt/live/staralliance.pro-0001/privkey.pem')
logging.info(u'Arbitartion websocket started')
# Initialise websocket connection on host 0.0.0.0 and port 8090
asyncio.get_event_loop().run_until_complete(websockets.serve(handler, '0.0.0.0', 8090, ssl=ctx))
asyncio.get_event_loop().run_forever()


