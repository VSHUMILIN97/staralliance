# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models


class Bittrex(models.Model):
    pair = models.CharField(max_length=50)
    High = models.FloatField()

    def publish(self):
        self.save()
