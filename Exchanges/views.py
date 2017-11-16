from django.shortcuts import render
from Exchanges.models import Bittrex
from django.utils import timezone
# Create your views here.
def Bittrex_view(request):



    book = Bittrex.objects.filter(published_date__lte=timezone.now()).order_by('published_date')


    return render(request, "Bittrex_template.html",  {'temp' : book})
