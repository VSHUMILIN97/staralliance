from django.shortcuts import render
from Exchanges.models import BittrexOHLC, BittrexVolume, BittrexTick
from django.views.generic import View
from mongo_db_connection import MongoDBConnection
# Create your views here.
# Для чистоты кода используем переменные с названиями bit_obj_tick вместо bitObjTick
# В_питоне_модно_с_граундами_писать , а не с АпперКейсомТипВотТак
# Python != Java :'(((


def index_view(request):
    return render(request, "index.html")


# Создан исключительно для проверки и отладки получения текстовых(паршенных) данных
def Bittrex_view(request, market=""):
    if market != "":
        market = market.upper()
        book = BittrexOHLC.objects.all().filter(PairName=market)
    else:
        book = BittrexOHLC.objects.all()
    return render(request, "Bittrex_template.html",  {'temp': book})  #


# Наша гордость. Работа и построение графиков, в прямом режиме делаются срезы из БД
# Предположительно это плохо. Возможно срезы нужно будет автоматизировать и убрать отсюда
# Класс отвечает за получение запроса по рынку(set as default if market = null.(BTC-1ST))
# В теории здесь должен остаться только блок управления контролами(Это не точно)
class ChartsView(View): # Класс для вывода графиков
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
        # В ней берем коллекцию и инсертим.
        test = db.Bittrex
        test.insert({'a': 1})
       # book = BittrexOHLC.objects.all().filter(PairName=market)
       # PublicApi = PublicAPI(PairName='PidorBaba', TimeStamp='2017.10.11')
       # PublicApi.save()
       # print(PublicApi.PairName)
        # Этих строк тут предположительно НЕ будет. Агреграция будет происходит по триггеру тикера В БЕСКОНЕЧНОМ режиме
        #testagr = TimeAggregator()
        #создает объект каждый раз, собственно нужен фикс. Строчку ниже не раскомменчивать до устранения!
        #testagr.OHLCaggregation(market)

        # Заполнение словарей QuerySetами для дальнейшей работы оных с JS
       # book1 = BittrexTick.objects.all().filter(PairName=market)
       # book_buy = BittrexVolume.objects.all().filter(PairName=market, OrderType='BUY')[:5]
       # book_sell = BittrexVolume.objects.all().filter(PairName=market, OrderType='SELL')[:5]
       # testaggr = BittrexOHLC.objects.all().filter(PairName=market, Aggregated=False)
        return render(request, 'charts.html', {})  # магия
