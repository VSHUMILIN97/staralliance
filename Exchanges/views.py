import datetime
from django.shortcuts import render
from django.views.generic import View
from mongo_db_connection import MongoDBConnection
from .TimeAggregator import arbitration_aggregate
# Create your views here.


def index_view(request):
    return render(request, "index.html")


# DEBUG ONLY WEB-PAGE
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


# CHARTS WEB-PAGE. NOT IN CURRENT USE. Still works.
class ChartsView(View):  #
    def get(self, request, exchange="", pair="", *args, **kwargs):
        b = MongoDBConnection().start_db()
        db = b.PiedPiperStock
        db.ExchsAndPairs.drop()
        ins = db.ExchsAndPairs
        exchlist = ['Bittrex', 'Gatecoin', 'LiveCoin', 'Liqui', 'Bleutrade', 'Poloniex',
                    'Binance', 'Exmo']  # пополняем вручную по мере поступления бирж
        for inner in range(0, len(exchlist)):
            exchname = exchlist[inner]
            pairlist = db[exchname].distinct('PairName')
            for secinner in pairlist:
                tdict = {'Exch': exchname, 'Pair': secinner}
                ins.insert(tdict)
                combinations = db.ExchsAndPairs.find().sort([('Exch', 1), ('Pair', 1)])
                # эту базу теперь можно еще где-нибудь поюзать

        if (pair != "") and (exchange != ""):
            return render(request, 'charts.html', {'pair': pair, 'exchange': exchange, 'exchList': sorted(exchlist),
                                                   'combinations': combinations})
        else:
            return render(request, 'choose.html', {'exchList': sorted(exchlist), 'combinations': combinations})


# We got two versions of our web-page. User is forced to USE the /old version.
class Comparison(View):
    def get(self, request, mode="", *args, **kwargs):
        if mode == 'new':
            return render(request, 'comparebeta.html', {})  # установить compare для другого отображения арбитража
        else:
            return render(request, 'compare.html', {})  # установить compare для другого отображения арбитража
