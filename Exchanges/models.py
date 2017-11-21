from django.db import models
from django.utils import timezone
import datetime
# Create your models here.

# Для чистоты кода используем переменные с названиями bit_obj_tick вместо bitObjTick
# В_питоне_модно_с_граундами_писать , а не с АпперКейсомТипВотТак
# Python != Java :'(((



class BittrexOHLC(models.Model):

    published_date = models.DateTimeField(default=timezone.now)
    PairName = models.CharField(max_length=60, null=True)
    High = models.FloatField(null=True)
    Low = models.FloatField(null=True)
    Last = models.FloatField(null=True)
    Volume = models.FloatField(null=True)
    BaseVolume = models.FloatField(null=True)
    TimeStamp = models.DateTimeField(null=True, default=datetime.datetime.now())
    Bid = models.FloatField(null=True)
    Ask = models.FloatField(null=True)
    OpenBuyOrders = models.CharField(max_length=40, null=True)
    OpenSellOrders = models.CharField(max_length=40, null=True)
    PrevDay = models.FloatField(null=True)
    BidDivAsk = models.FloatField(null=True)

    def setVals(self):

        self.save()




class BittrexTick(models.Model):
    PairName = models.CharField(max_length=60, null=True)
    TimeStamp = models.CharField(max_length=60, default=timezone.now)
    Tick = models.FloatField()

    def saveModel(self):
        self.save()


class BittrexVolume(models.Model):
    PairName = models.CharField(max_length=20)
    IdOrder = models.BigIntegerField()
    TimeStamp = models.CharField(max_length=60, default=timezone.now)
    Quantity = models.FloatField()
    Price = models.FloatField()
    Total = models.FloatField()
    FillType = models.CharField(max_length=25)
    OrderType = models.CharField(max_length=15)

    def autoSave(self):
        self.save()



