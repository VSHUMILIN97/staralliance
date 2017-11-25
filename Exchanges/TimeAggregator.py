from  Exchanges import models
import datetime
import time
import iso8601
from datetime import datetime,tzinfo,timedelta
from django.utils import timezone, datetime_safe
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
        global tempLast, tempPrevday, tempAggregation
        if market == "":
            market = 'BTC-1ST'

        #бал рот этого вашего времени, иззвините. Антихайп
        """https://djbook.ru/rel1.8/topics/i18n/timezones.html"""
        print(BittrexOHLC.objects.datetimes('TimeStamp', 'second')[1])
        faketime = (2017, 11, 25, 18, 10, 0, 1, 0, 0)
        fakestart = time.mktime(tuple(faketime))
        fakelenght = len(BittrexOHLC.objects.datetimes('TimeStamp', 'second'))
        for i in range(0, fakelenght):
            if timezone.utc(BittrexOHLC.objects.datetimes('TimeStamp', 'second')[i+1]) - timezone.utc(BittrexOHLC.objects.datetimes('TimeStamp', 'second')[i]) > fakestart:
                tempAggregation = models.BittrexOHLC.objects.filter(PairName=market, Aggregated=False, TimeStamp=BittrexOHLC.objects.datetimes('TimeStamp', 'second')[i]).aggregate(Max('High'), Min('Low'))
                tempPrevday = models.BittrexOHLC.objects.filter(PairName=market, Aggregated=False, TimeStamp=BittrexOHLC.objects.datetimes('TimeStamp', 'second')[i]).values('PrevDay', 'TimeStamp')[0]
                tempLast = models.BittrexOHLC.objects.filter(PairName=market, Aggregated=False, TimeStamp=BittrexOHLC.objects.datetimes('TimeStamp', 'second')[i]).values('Last').latest('Last')

                bit_obj_ohlc = BittrexOHLC(PairName=market, High=tempAggregation.get('High__max'),
                                           Low=tempAggregation.get('Low__min'), Last=tempLast.get('Last'),
                                           TimeStamp=tempPrevday.get('TimeStamp'), PrevDay=tempPrevday.get('PrevDay'),
                                           Aggregated=True)
                bit_obj_ohlc.save()
            else:
                """tempAggregation = models.BittrexOHLC.objects.filter(PairName=market, Aggregated=False,TimeStamp=BittrexOHLC.objects.datetimes('TimeStamp', 'second')[i+1]).aggregate(Max('High'), Min('Low'))
                tempPrevday = models.BittrexOHLC.objects.filter(PairName=market, Aggregated=False, TimeStamp=BittrexOHLC.objects.datetimes('TimeStamp', 'second')[i+1]).values('PrevDay', 'TimeStamp')[0]
                tempLast = models.BittrexOHLC.objects.filter(PairName=market, Aggregated=False, TimeStamp=BittrexOHLC.objects.datetimes('TimeStamp', 'second')[i+1]).values('Last').latest('Last')"""
        #
        #Данный метод не дает возможности отслеживать таймлайн/ Нужен фикс
        #
        print(tempAggregation, ' ', tempPrevday, ' ', tempLast)

        bit_obj_ohlc = BittrexOHLC(PairName=market, High=tempAggregation.get('High__max'), Low=tempAggregation.get('Low__min'), Last=tempLast.get('Last'), TimeStamp=tempPrevday.get('TimeStamp'), PrevDay=tempPrevday.get('PrevDay'), Aggregated=True)
        bit_obj_ohlc.save()

    def Volumeaggregation(self):
        return None

    def Tickaggregation(self):
        return None