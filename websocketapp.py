import asyncio
import time
import json
import logging
import redis
import websockets
from Exchanges.ExchangeAPI.PairDataNOTAPI import approved_keys
from PiedPiper.settings import REDIS_HOST, REDIS_PORT


logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename='/var/log/cryptopiper/websockets.log')
r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

p = r.pubsub()
p.psubscribe('s-*')


# Function, that provides connect between client and server.
# Works with async to prevent interrupting main thread.
async def arbitration_socket(websocket, path):
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
                    await websocket.send(json.dumps([msg.split('/')[1] + '/'
                                                     + msg.split('/')[2],
                                                     r.get(msg).decode('utf-8')]))
            except TypeError:
                pass
        time.sleep(0.001)


logging.info(u'Arbitartion websocket started')
# Initialise websocket connection on host 127.0.0.1 and port 8090
asyncio.get_event_loop().run_until_complete(websockets.serve(arbitration_socket, '127.0.0.1', 8090))
asyncio.get_event_loop().run_forever()



