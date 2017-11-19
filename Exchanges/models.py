from django.db import models
from django.utils import timezone

import requests
import json
import time


# Create your models here.

class Bittrex(models.Model):
    published_date = models.DateTimeField(default=timezone.now)
    PairName = models.CharField(max_length=60)
    High = models.FloatField()
    Low = models.FloatField()
    Last = models.FloatField()
    Volume = models.FloatField()
    BaseVolume = models.FloatField()
    TimeStamp = models.DateTimeField()
    Bid = models.FloatField()
    Ask = models.FloatField()
    OpenBuyOrders = models.CharField(max_length=40)
    OpenSellOrders = models.CharField(max_length=40)
    PrevDay = models.FloatField()

    def setVals(self):

        self.save()

    #
    """
    def loadFromExchange(self, json_data):

        PAINAME = json_data
        HIGH = json_data
        LOW = json_data
        VOLUME = json_data
        LAST = json_data
        BASEVOLUME = json_data
        TIMESTAMP = json_data
        BID = json_data
        ASK = json_data
        OPENBUYORDERS = json_data
        OPENSELLORDER = json_data
        PREVDAY = json_data
        CURRENCY = json_data
        CURRENCYLONG = json_data


        self.save()

    """


