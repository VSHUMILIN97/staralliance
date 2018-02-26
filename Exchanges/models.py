from django.db import models
from django.utils import timezone
# Create your models here.


"""class PublicAPI(Document):
    PairName = StringField(max_length=12)
    TimeStamp = DateTimeField(default=timezone.now, help_text='returned date')
    Tick = FloatField()
    Aggregated = BooleanField(default=False)"""

"""
#
#
NOT IN WORK. CLOSE THIS SCRIPT. WE DO NOT USE THE FULL ORM OPPORTUNITIES
#
#
"""


class BittrexOHLC(models.Model):

    published_date = models.DateTimeField(default=timezone.now)
    PairName = models.CharField(max_length=60, null=True)
    High = models.FloatField(null=True)
    Low = models.FloatField(null=True)
    Last = models.FloatField(null=True)
    TimeStamp = models.DateTimeField(null=True, default=timezone.now)
    PrevDay = models.FloatField(null=True)
    Aggregated = models.BooleanField(default=False)

    def set_values(self):
        self.save()


class BittrexTick(models.Model):
    PairName = models.CharField(max_length=60, null=True)
    TimeStamp = models.DateTimeField(default=timezone.now)
    Tick = models.FloatField()
    Aggregated = models.BooleanField(default=False)

    def save_model(self):
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

    def auto_save(self):
        self.save()



