# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 19:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exchanges', '0003_auto_20171122_0044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bittrexohlc',
            name='TimeStamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 22, 0, 50, 26, 916629), null=True),
        ),
    ]
