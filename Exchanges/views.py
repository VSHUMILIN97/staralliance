import datetime
from django.shortcuts import render
from django.views.generic import View
from mongo_db_connection import MongoDBConnection
from .TimeAggregator import arbitration_aggregate
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
    slice = db.temporaryTick.find({'PairName': 'BTC-1ST'}).limit(5)
    return render(request, "Bittrex_template.html",  {'temp': slice})  #


# Наша гордость. Работа и построение графиков, в прямом режиме делаются срезы из БД
# Предположительно это плохо. Возможно срезы нужно будет автоматизировать и убрать отсюда
# Класс отвечает за получение запроса по рынку(set as default if market = null.(BTC-1ST))
# В теории здесь должен остаться только блок управления контролами(Это не точно)
class ChartsView(View):  # Класс для вывода графиков
    def get(self, request, exchange="", pair="", *args, **kwargs):
        b = MongoDBConnection().start_db()
        db = b.PiedPiperStock
        db.ExchsAndPairs.drop()
        ins = db.ExchsAndPairs
        exchlist = ['Bittrex', 'Gatecoin', 'LiveCoin', 'Liqui', 'Bleutrade', 'Poloniex',
                    'Binance']  # пополняем вручную по мере поступления бирж
        for inner in range(0, len(exchlist)):
            exchname = exchlist[inner]
            pairlist = db[exchname + 'Tick'].distinct('PairName')
            for secinner in pairlist:
                tdict = {'Exch': exchname, 'Pair': secinner}
                ins.insert(tdict)
        combinations = db.ExchsAndPairs.find()  # эту базу теперь можно еще где-нибудь поюзать

        if (pair != "") and (exchange != ""):
            pair = pair.upper()

            # ALEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEERT тут надо переделать

            testdictOHLC = db.Bittrex.find({'PairName': pair, 'Aggregated': True})
            testdictMHistSell = db.BittrexMHist.find({'PairName': pair, 'OrderType': 'SELL', 'Aggregated': True})
            testdictMHistBuy = db.BittrexMHist.find({'PairName': pair, 'OrderType': 'BUY', 'Aggregated': True})
            tick = db[exchange + 'Tick'].find({'PairName': pair, 'Aggregated': True})

            return render(request, 'charts.html', {'testingOHLC': testdictOHLC, 'testingMHistSell': testdictMHistSell,
                                                   'testingMHistBuy': testdictMHistBuy, 'ticks': tick,
                                                   'pair': pair, 'exchange': exchange,
                                                   'exchList': sorted(exchlist), 'combinations': combinations})
        else:
            # все это надо отсюда куда-нибудь унести
            return render(request, 'choose.html', {'exchList': sorted(exchlist), 'combinations': combinations})


class Comparison(View):
    def get(self, request, mode="",*args, **kwargs):
        if (mode == 'new'):
            return render(request, 'comparebeta.html', {})  # установить compare для другого отображения арбитража
        else:
            return render(request, 'compare.html', {})  # установить compare для другого отображения арбитража
