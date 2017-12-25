import asyncio
from threading import Thread

from django.shortcuts import render
from django.views.generic import View
from mongo_db_connection import MongoDBConnection
from .TimeAggregator import arbitration_aggregate
from .websockets import returner


# Create your views here.
# Для чистоты кода используем переменные с названиями bit_obj_tick вместо bitObjTick
# В_питоне_модно_с_граундами_писать , а не с АпперКейсомТипВотТак
# Python != Java :'(((


def index_view(request):
    return render(request, "index.html")


# Создан исключительно для проверки и отладки получения текстовых(паршенных) данных
def Bittrex_view(request, market=""):
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    if market != "":
        market = market.upper()
        testdictOHLC = db.Bittrex.find({'PairName': market, 'Aggregated': True})
    else:
        testdictOHLC = db.Bittrex.find({'PairName': 'BTC-ETH', 'Aggregated': True})
    slice = db.temporaryTick.find({'PairName': 'BTC-1ST'}).limit(1)
    return render(request, "Bittrex_template.html",  {'temp': slice})  #


# Наша гордость. Работа и построение графиков, в прямом режиме делаются срезы из БД
# Предположительно это плохо. Возможно срезы нужно будет автоматизировать и убрать отсюда
# Класс отвечает за получение запроса по рынку(set as default if market = null.(BTC-1ST))
# В теории здесь должен остаться только блок управления контролами(Это не точно)
class ChartsView(View):  # Класс для вывода графиков
    def get(self, request, market="", *args, **kwargs):

        if market != "":
            # Переводим имя пары из URL в upper case
            market = market.upper()
            # Обращаемся к модели BittrexOHLC из models.py
        else:
            market = 'BTC-1ST'
        # Инициализируем коннект, возвращаем объект коннекта из mongo_db_connection.
        b = MongoDBConnection().start_db()
        # Захватываем ту БД, что хотим
        db = b.PiedPiperStock
        # В ней берем коллекцию и делаем выборку.
        # Создаем 4 словаря. (Для MarketHistory срезы по Sell и Buy)
        testdictOHLC = db.Bittrex.find({'PairName': market, 'Aggregated': True})
        testdictMHistSell = db.BittrexMHist.find({'PairName': market, 'OrderType': 'SELL', 'Aggregated': True})
        testdictMHistBuy = db.BittrexMHist.find({'PairName': market, 'OrderType': 'BUY', 'Aggregated': True})
        testdictTick = db.BittrexTick.find({'PairName': market, 'Aggregated': True})
        return render(request, 'charts.html', {'testingOHLC': testdictOHLC, 'testingMHistSell': testdictMHistSell,
                                               'testingMHistBuy': testdictMHistBuy, 'testingTick': testdictTick})



class Comparison(View):


    def get(self, request, *args, **kwargs):
       #market = 'BTC-1ST'
       #b = MongoDBConnection().start_db()
       #db = b.PiedPiperStock
       #db.temporaryTick.drop()
       #arbitration_aggregate()

       asyncio.get_event_loop().run_until_complete(returner())
       asyncio.get_event_loop().run_forever()#
       ##ticks = list(db.temporaryTick.find())
       #columns = len(db.temporaryTick.distinct('Exch'))
       #rows = len(db.temporaryTick.distinct('PairName'))
       #cnames = db.temporaryTick.distinct('Exch')
       #rnames = db.temporaryTick.distinct('PairName')

       return render(request, 'compare.html', {})
                     # {'ticks': ticks, 'market': market, 'columns': columns, 'rows': rows, 'cnames': cnames,
                      # 'rnames': rnames})

