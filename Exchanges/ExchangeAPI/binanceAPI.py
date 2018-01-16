# https://www.binance.com/api/v3/ticker/bookTicker
import json
import logging
from django.utils import timezone
import requests
from mongo_db_connection import MongoDBConnection

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)
