from django.http import JsonResponse
from django.shortcuts import render
from Exchanges.models import Bittrex
from django.views.generic import View
from django.shortcuts import render
from Exchanges.models import Bittrex
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from Exchanges.BittrexObjCreate import api_get_getmarketsummaries
from django.utils import timezone
# Create your views here.
def Bittrex_view(request):

    #api_get_getmarketsummaries()
    book = Bittrex.objects.all().filter(PairName='BTC-1ST')
    return render(request, "Bittrex_template.html",  {'temp': book})

class ChartsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts.html')