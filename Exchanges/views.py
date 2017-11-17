from django.shortcuts import render
from Exchanges.models import Bittrex
from Exchanges.BittrexObjCreate import api_get_getmarketsummaries
from django.utils import timezone
# Create your views here.
def Bittrex_view(request):

    #api_get_getmarketsummaries()
    book = Bittrex.objects.all()
    return render(request, "Bittrex_template.html",  {'temp' : book})
