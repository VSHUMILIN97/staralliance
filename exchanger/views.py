import json

from django.shortcuts import render

# Create your views here.
from django.utils.safestring import mark_safe
from django.views import View


class Exchanger(View):
    def get(self, request):
        return render(request, 'exchanger.html', {'msg': 'LULOMEGA'})


def room(request, room_name):
    return render(request, 'exchanger.html', {'room_name_json': mark_safe(json.dumps(room_name))})
