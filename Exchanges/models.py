from django.db import models
from django.utils import timezone


# Create your models here.

class Bittrex(models.Model):
    published_date = models.DateTimeField(default=timezone.now)
    PairName = models.CharField(max_length=50)
    High = models.FloatField()

    # LOW = models.Low()
    # VOLUME = models.Volume()
    # LAST = models.Last()
    # BASEVOLUME = models.BaseVolume()
    # TIMESTAMP = models.TimeStamp()
    # BID = models.Bid()
    # ASK = models.Ask()
    # OPENBUYORDERS = models.OpenBuyOrders()
    # OPENSELLORDERS = models.OpenSellOrders()
    # PREVDAY = models.PrevDay()
    # CURRENCY = models.Currency()
    # CURRENCYLONG = models.CurrencyLong()



    # author = models.ForeignKey('auth.User')
    # title = models.CharField(max_length=200)
    # text = models.TextField()
    # created_date = models.DateTimeField(
    #    default=timezone.now)
    # published_date = models.DateTimeField(
    #    blank=True, null=True)



    def setVals(self):
        self.save()

    def getUrl(self):
        return "https://bittrex.com/api/v1.1/public/getmarketsummaries"

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
