# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 19:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exchanges', '0002_bittrexvolume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bittrexohlc',
            name='TimeStamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 22, 0, 44, 8, 307582), null=True),
        ),
    ]