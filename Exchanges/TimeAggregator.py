from  Exchanges import models
import datetime
import time
from mongo_db_connection import MongoDBConnection
import iso8601
from datetime import datetime,tzinfo,timedelta
from django.utils import timezone, datetime_safe




class TimeAggregator:

    def __init__(self):
        None
    # Предстоит тяжелая и нудная работа =) https://docs.djangoproject.com/en/1.11/topics/db/aggregation/

    def OHLCaggregation(self, PairName, ServerTime):
        b = MongoDBConnection().start_db()
        db = b.PiedPiperStock
        test = db.Bittrex

    None

    def Volumeaggregation(self):
        return None

    def Tickaggregation(self):
        return None
