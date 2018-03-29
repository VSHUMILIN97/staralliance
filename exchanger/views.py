import json

from django.shortcuts import render

# Create your views here.
from django.utils.safestring import mark_safe
from django.views import View


class Exchanger(View):
    def get(self, request):
        return render(request, 'exchanger.html')
