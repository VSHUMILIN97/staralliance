import redis
import sys
import os.path
import logging

import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../djangopiper'))
from PiedPiper.settings import REDIS_HOST, REDIS_PORT

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)
r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

p = r.pubsub()
p.subscribe('keychannel')


def approved_keys():
    whole_data = []
    key_list = []
    pairs = []
    clear_pairs = []

    for key in r.scan_iter():
        whole_data.append({key.decode('utf-8'): r.get(key).decode('utf-8')})

    for item in whole_data:
        for key in item:
            some_var = str(key).split('/')
            pairs.append(some_var[2])

    for item in pairs:
        if pairs.count(item) >= 2:
            if item not in clear_pairs:
                clear_pairs.append(item)

    for item in whole_data:
        for key in item:
            some_var = str(key).split('/')
            if some_var[2] in clear_pairs:
                key_list.append(key)

    return key_list

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
        except AttributeError:
            time.sleep(0.001)


