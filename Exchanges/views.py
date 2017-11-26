import random
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import time
import asyncio
import django
from django.http import JsonResponse
from multiprocessing import Process
from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render
from Exchanges.models import BittrexOHLC
from Exchanges.models import BittrexTick
from Exchanges.models import BittrexVolume
from .tick_exchparser import SeedCall, RandomSeed
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from Exchanges.BittrexObjCreate import api_get_getmarkethistory
from Exchanges.BittrexObjCreate import api_get_getmarketsummaries
from Exchanges.BittrexObjCreate import api_get_getticker
#from Exchanges.TimeAggregator import TimeAggregator
from django.utils import timezone

# Create your views here.
# Для чистоты кода используем переменные с названиями bit_obj_tick вместо bitObjTick
# В_питоне_модно_с_граундами_писать , а не с АпперКейсомТипВотТак
# Python != Java :'(((

def index_view(request):
    return render(request, "index.html")

def Bittrex_view(request, market=""):

    api_get_getmarketsummaries()
    if market != "":
        market = market.upper()
        book = BittrexOHLC.objects.all().filter(PairName=market)
    else:
        book = BittrexOHLC.objects.all()
    return render(request, "Bittrex_template.html",  {'temp': book})  #


class ChartsView(View): # Класс для вывода графиков
    def get(self, request, market="", *args, **kwargs):
        import multiprocessing
        #Вызов функции опроса бирж. Надо перенести поток в дэмоник.

        if market != "":
            # Переводим имя пары из URL в upper case
            market = market.upper()
            # Обращаемся к модели BittrexOHLC из models.py
        else:
            market = 'BTC-1ST'

        book = BittrexOHLC.objects.all().filter(PairName=market)


        #testagr = TimeAggregator()
        #создает объект каждый раз, собственно нужен фикс. Строчку ниже не раскомменчивать до устранения!
        #testagr.OHLCaggregation(market)

        book1 = BittrexTick.objects.all().filter(PairName=market)
        book_buy = BittrexVolume.objects.all().filter(PairName=market, OrderType='BUY')[:5]
        book_sell = BittrexVolume.objects.all().filter(PairName=market, OrderType='SELL')[:5]
        testaggr = BittrexOHLC.objects.all().filter(PairName=market, Aggregated=False)

        #join мешает, потому что результат цикла нельзя вогнать в основной трэд
        testp = Process(target=SeedCall)
        testp.start()
        #testp.join()
        return render(request, 'charts.html', {'temp': book, 'temp1': book1, 'market': market, 'buyBook': book_buy, 'sellBook': book_sell, 'testAggr': testaggr})  #магия
