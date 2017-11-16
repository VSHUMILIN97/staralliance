# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Bittrex

# Create your views here.
def bittrex(request):
    temp = Bittrex(pair='utc-utc', High=0.124)
    temp.save()
    posts = Bittrex.objects.all()
    return render(request, 'bittrex/bittrex.html', {'bittrex':posts})