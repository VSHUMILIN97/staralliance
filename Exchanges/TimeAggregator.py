from  Exchanges import models
from django.utils import timezone
from django.db.models import Count
from django.db.models import Max
from django.db.models import Min


class TimeAggregator:

    def __init__(self):
        self.OHLCaggregation()

    """Предстоит тяжелая и нудная работа =) https://docs.djangoproject.com/en/1.11/topics/db/aggregation/"""
    def OHLCaggregation(self):
        temph = models.BittrexOHLC.objects.values('PairName').annotate(High=Max('High'))
        templ = models.BittrexOHLC.objects.values('PairName').annotate(Low=Min('Low'))
        temppd = models.BittrexOHLC.objects.values('PrevDay')
        templast = models.BittrexOHLC.objects.values('Last')
        templast_len = len(templast)
        print(templast, ' ', templ, ' ', temppd, ' ', temph)
        dict = {'High': temph, 'Low': templ, 'PrevDay': temppd, 'Last': templast[templast_len-1], 'TimeStamp': '010101'}
        return dict

    def Volumeaggregation(self):
        return None

    def Tickaggregation(self):
        return None