from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render
from Exchanges.models import BittrexOHLC
from Exchanges.models import BittrexTick
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from Exchanges.BittrexObjCreate import api_get_getmarketsummaries
from Exchanges.BittrexObjCreate import api_get_getticker
from django.utils import timezone
# Create your views here.
def Bittrex_view(request, market=""):

    #api_get_getmarketsummaries()
    #api_get_getticker()
    if market != "":
        market = market.upper()
        book = BittrexOHLC.objects.all().filter(PairName=market)
    else:
        book = BittrexOHLC.objects.all()
    return render(request, "Bittrex_template.html",  {'temp': book})  #

class ChartsView(View):
    def get(self, request, market="", *args, **kwargs):
        api_get_getticker(market)
        if market != "":
            market = market.upper()
            book = BittrexOHLC.objects.all().filter(PairName=market)
        else:
            market = 'BTC-1ST'
            book = BittrexOHLC.objects.all().filter(PairName=market)
        book1 = BittrexTick.objects.all().filter(PairName=market)
        return render(request, 'charts.html', {'temp': book, 'temp1': book1, 'market': market})  #магия
