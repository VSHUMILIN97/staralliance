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
    TimeStamp = models.DateTimeField(null=True, default=timezone.now)
    PrevDay = models.FloatField(null=True)
    Aggregated = models.BooleanField(default=False)

    def setVals(self):

        self.save()




class BittrexTick(models.Model):
    PairName = models.CharField(max_length=60, null=True)
    TimeStamp = models.DateTimeField(default=timezone.now)
    Tick = models.FloatField()
    Aggregated = models.BooleanField(default=False)

    def saveModel(self):
        self.save()


class BittrexVolume(models.Model):
    PairName = models.CharField(max_length=20)
    IdOrder = models.BigIntegerField()
    TimeStamp = models.DateTimeField(default=timezone.now)
    Quantity = models.FloatField()
    Price = models.FloatField()
    Total = models.FloatField()
    FillType = models.CharField(max_length=25)
    OrderType = models.CharField(max_length=15)
    Aggregated = models.BooleanField(default=False)

    def autoSave(self):
        self.save()



