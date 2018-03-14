import json
import redis
from django.shortcuts import render
from django.views.generic import View
from PiedPiper.settings import REDIS_DEFAULT_PORT, REDIS_DEMOS_HOST
from mongo_db_connection import MongoDBConnection
from Exchanges.ExchangeAPI.PairDataNOTAPI import approved_exchanges, approved_pairs, approved_keys
conn_r = redis.ConnectionPool(host=REDIS_DEMOS_HOST, port=REDIS_DEFAULT_PORT, db=0)
r = redis.Redis(connection_pool=conn_r)
# Create your views here.


def keys(dictionary):
    repaired_map = []
    state_map = state_saver()
    for item in state_map:
        for preload in dictionary:
            if str(preload).endswith(item):
                repaired_map.append(preload)
                break
    return repaired_map


def state_saver():
    cleared_state = []
    pairs = sorted(approved_pairs())
    exchs = sorted(approved_exchanges())
    for pair in pairs:
        for exch in exchs:
            cleared_state.append(exch + '/' + pair)
    return cleared_state


def state_getter(clear_map):
    lul = []
    for item in clear_map:
        ok_state = item.split('/')
        lul.append({ok_state[1] + '/' + ok_state[2]: r.get(item).decode('utf-8')})
    return lul


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
            return render(request, 'compare.html', {'pairs': json.dumps(sorted(approved_pairs())), 'exchs':
                                                    json.dumps(sorted(approved_exchanges())),
                                                    'ticks': json.dumps(state_getter(keys(approved_keys())))})
            # установить compare для другого отображения арбитража
