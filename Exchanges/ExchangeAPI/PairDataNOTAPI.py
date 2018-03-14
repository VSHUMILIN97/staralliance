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


def approved_pairs():
    pair_data = []
    non_return_pairs = []
    return_pairs = []
    for key in r.scan_iter():
        pair_data.append({key.decode('utf-8'): r.get(key).decode('utf-8')})

    for item in pair_data:
        for key in item:
            split_var = str(key).split('/')
            non_return_pairs.append(split_var[2])
    for item in non_return_pairs:
        if non_return_pairs.count(item) >= 2:
            if item not in return_pairs:
                return_pairs.append(item)

    return return_pairs


def approved_exchanges():
    exch_data = []
    return_exch = []
    for key in r.scan_iter():
        exch_data.append({key.decode('utf-8'): r.get(key).decode('utf-8')})

    for item in exch_data:
        for key in item:
            split_var = str(key).split('/')
            if split_var[1] not in return_exch:
                return_exch.append(split_var[1])
    return return_exch


def approved_keys():
    whole_data = []
    key_list = []
    pairs = []
    clear_pairs = []

    for key in r.scan_iter():
        whole_data.append({key.decode('utf-8'): r.get(key).decode('utf-8')})

    for item in whole_data:
        for key in item:
            try:
                some_var = str(key).split('/')
                pairs.append(some_var[2])
            except IndexError:
                pass

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
