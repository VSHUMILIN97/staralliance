from  Exchanges import models
from django.utils import timezone
from django.db.models import Count
from django.db.models import Max
from django.db.models import Min
from .models import BittrexOHLC
from itertools import chain
from django.db.models import F
from django.db.models import Avg



class TimeAggregator:

    def __init__(self):

        """Предстоит тяжелая и нудная работа =) https://docs.djangoproject.com/en/1.11/topics/db/aggregation/"""
    def OHLCaggregation(self, market):
        if market == "":
            market == 'BTC-1ST'
        tempAggregation = models.BittrexOHLC.objects.filter(PairName=market).aggregate(Max('High'), Min('Low'))
        tempPrevday = models.BittrexOHLC.objects.filter(PairName=market).values('PrevDay', 'TimeStamp')[0]
        tempLast = models.BittrexOHLC.objects.filter(PairName=market).values('Last').latest('Last')
        #
        #Данный метод не дает возможности отслеживать таймлайн/ Нужен фикс
        #
        print(tempAggregation, ' ', tempPrevday, ' ', tempLast)

        bit_obj_ohlc = BittrexOHLC(PairName=market, High=tempAggregation.get('High__max'), Low=tempAggregation.get('Low__min'), Last=tempLast.get('Last'), TimeStamp=tempPrevday.get('TimeStamp'), PrevDay=tempPrevday.get('PrevDay'), Aggregated=True)
        bit_obj_ohlc.save()

        #Добавить запись в модель, во вьюхах сортировать по полю aggregated

    def Volumeaggregation(self):
        return None

    def Tickaggregation(self):
        return None