import json
import redis
from channels.generic.websocket import WebsocketConsumer
import logging
from Exchanges.ExchangeAPI.PairDataNOTAPI import approved_keys
from PiedPiper.settings import LOCAL_SERVICE_HOST, REDIS_DEFAULT_PORT


# class ArbitrationConsumer(WebsocketConsumer):
#
#     def connect(self):
#         self.accept()
#         r = redis.StrictRedis(host=LOCAL_SERVICE_HOST, port=REDIS_DEFAULT_PORT, db=0)
#         # r = redis.Redis(connection_pool=conn_r)
#         p = r.pubsub()
#         while 1:
#             # self.send(text_data="[Welcome]")
#             p.psubscribe('s-*')
#             # After the connect with client was established open connect to MongoDB
#             all_the_current_keys = approved_keys()
#             # Register.
#             try:
#                 while True:
#                     message = p.get_message()
#                     if message:
#                         msg = dict(message)['data']
#                         if msg == 1:
#                             continue
#                         else:
#                             msg = dict(message)['data'].decode('utf-8')
#                             exch = str(msg.split('/')[1])
#                             pair = str(msg.split('/')[2])
#                             pretick = r.get(msg)
#                             tick = str(pretick.decode('utf-8'))
#                         if msg in all_the_current_keys:
#                             self.send(text_data=json.dumps([exch + '/' + pair, tick]))
#             except BaseException:
#                 pass
#
#     def disconnect(self, code):        logging.info('RIP connection')

from channels.consumer import SyncConsumer


class ArbConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept",
        })

        r = redis.StrictRedis(host=LOCAL_SERVICE_HOST, port=REDIS_DEFAULT_PORT, db=0)
        # r = redis.Redis(connection_pool=conn_r)
        p = r.pubsub()
        while 1:
            # self.send(text_data="[Welcome]")
            p.psubscribe('s-*')
            # After the connect with client was established open connect to MongoDB
            all_the_current_keys = approved_keys()
            # Register.
            try:
                while True:
                    message = p.get_message()
                    if message:
                        msg = dict(message)['data']
                        if msg == 1:
                            continue
                        else:
                            msg = dict(message)['data'].decode('utf-8')
                            exch = str(msg.split('/')[1])
                            pair = str(msg.split('/')[2])
                            pretick = r.get(msg)
                            tick = str(pretick.decode('utf-8'))
                        if msg in all_the_current_keys:
                            self.send({
                                "type": "websocket.send",
                                "text": json.dumps([exch + '/' + pair, tick]),
                            })
            except BaseException:
                pass
