# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 11:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BittrexOHLC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('PairName', models.CharField(max_length=60, null=True)),
                ('High', models.FloatField(null=True)),
                ('Low', models.FloatField(null=True)),
                ('Last', models.FloatField(null=True)),
                ('Volume', models.FloatField(null=True)),
                ('BaseVolume', models.FloatField(null=True)),
                ('TimeStamp', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('Bid', models.FloatField(null=True)),
                ('Ask', models.FloatField(null=True)),
                ('OpenBuyOrders', models.CharField(max_length=40, null=True)),
                ('OpenSellOrders', models.CharField(max_length=40, null=True)),
                ('PrevDay', models.FloatField(null=True)),
                ('BidDivAsk', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BittrexTick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PairName', models.CharField(max_length=60, null=True)),
                ('TimeStamp', models.CharField(default=django.utils.timezone.now, max_length=60)),
                ('Tick', models.FloatField()),
            ],
        ),
    ]
