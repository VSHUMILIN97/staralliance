from datetime import datetime
import time
from mongo_db_connection import MongoDBConnection
import dateutil.parser
from datetime import datetime, tzinfo, timedelta
from django.utils import timezone, datetime_safe
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


def OHLCaggregation(ServerTime):
    import pymongo
    global highest_value, endingtime, startingtime
    global lowest_value
    global LastValue
    global PrevDayValue
    global TimeStamp
    global PairName
    logging.info(u'..OHLCAggregation started at..' + str(ServerTime))
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    exchlist = ['Bittrex']
    for inner in range(0, len(exchlist)):
        exchname = exchlist[inner]
        pairlist = db[exchname].distinct('PairName')
        logging.info(u'Going through..' + str(exchname))
        # Подобная штука не работает, он тщательно отказывается видеть вложенный цикл.
        # for secinner in range(0, len(pairlist)):
        #
        for secinner in pairlist:
            # All Matches in DB
            delayActivation = timedelta(minutes=5)
            half_delay = timedelta(minutes=2, seconds=30)
            # Starting time magic
            timer_at_first = db[exchname].find({'PairName': secinner, 'Mod': False}, {'TimeStamp': True}).limit(1)
            #
            enter_counter = db[exchname].find({'PairName': secinner, 'Aggregated': True},
                                              {'TimeStamp': True}).count()
            time_after_aggregation = db[exchname].find({'PairName': secinner, 'Aggregated': True},
                                                       {'TimeStamp': True})\
                .sort('TimeStamp', pymongo.DESCENDING).limit(1)
            if enter_counter > 0:
                for subintosub in time_after_aggregation:
                    startingtime = dateutil.parser.parse(str(subintosub['TimeStamp']))
                    startingtime = startingtime + half_delay
            else:
                for subinto in timer_at_first:
                     startingtime = dateutil.parser.parse(str(subinto['TimeStamp']))
            #
            mergingtime = startingtime + delayActivation
            while 1:
                try:
                    if mergingtime < ServerTime:
                        # High Работа с глобальными переменными. Переприсвоится дальше.
                        highest_value = 0
                        endingtime = startingtime + delayActivation
                        # Low Записываем значение из одномерного словаря (Это можно отрефакторить - WELCOME!)
                        low_val_dict = db[exchname].find({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                                         {'$gte': startingtime, '$lt': endingtime}}, {'Low': True}).limit(1)
                        # Last Пишем первый объект из коллекции. Так и не разобрались с полем.
                        # Поиск по паре, полю Mod - Modified/ TimeStamp в разрезе от startingtime до endingtime
                        last_val_dict = db[exchname].find({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                                          {'$gte': startingtime, '$lt': endingtime}},
                                                          {'Last': True}).limit(1)
                        #
                        pair_matcher = db[exchname].find({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                                         {'$gte': startingtime, '$lt': endingtime}})
                        #
                        prev_day_dict = db[exchname].find({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                                          {'$gte': startingtime, '$lt': endingtime}}, {'PrevDay': True})
                        for subinLow in low_val_dict:
                            lowest_value = subinLow['Low']
                        # Last
                        for subinLast in last_val_dict:
                            LastValue = subinLast['Last']
                        # PrevDay
                        for subinPrevDay in prev_day_dict:
                            PrevDayValue = subinPrevDay['PrevDay']
                        #
                        for trdinner in pair_matcher:
                            if trdinner['High'] > highest_value:
                                highest_value = trdinner['High']
                            if trdinner['Low'] < lowest_value:
                                lowest_value = trdinner['Low']
                        tempdict = {'PairName': secinner, 'High': highest_value,
                                    'Low': lowest_value, 'TimeStamp': startingtime + half_delay, 'Last': LastValue,
                                    'PrevDay': PrevDayValue, 'Aggregated': True}
                        db[exchname].insert(tempdict)
                        db[exchname].update({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                            {'$gte': startingtime, '$lt': endingtime}}, {'$set': {'Mod': True}}, multi=True)
                        # Конец работы с циклом, переход на следующие 5 минут времени

                        startingtime = startingtime + delayActivation
                        mergingtime = mergingtime + delayActivation
                    else:
                        break
                except:
                    logging.error(u'OHLCAgg')
        logging.info(u'Check' + exchname + u'collection')


def Volumeaggregation(ServerTime):
    import pymongo
    logging.info(u'..VolumeAggregation started at..' + str(ServerTime))
    global sell_data, endingtime, startingtime, buy_data, TimeStamp, PairName, sold_data, bought_data
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    exchlist = ['BittrexMHist']
    for inner in range(0, len(exchlist)):
        exchname = exchlist[inner]
        pairlist = db[exchname].distinct('PairName')
        logging.info(u'Going through..' + exchname)
        #
        for secinner in pairlist:
            # All Matches in DB
            delayActivation = timedelta(minutes=5)
            half_delay = timedelta(minutes=2, seconds=30)
            # Starting time magic
            timer_at_first = db[exchname].find({'PairName': secinner, 'Mod': False}, {'TimeStamp': True}).limit(1)
            #
            enter_counter = db[exchname].find({'PairName': secinner, 'Aggregated': True},
                                              {'TimeStamp': True}).count()
            time_after_aggregation = db[exchname].find({'PairName': secinner, 'Aggregated': True},
                                                       {'TimeStamp': True})\
                .sort('TimeStamp', pymongo.DESCENDING).limit(1)
            if enter_counter > 0:
                for subintosub in time_after_aggregation:
                    startingtime = dateutil.parser.parse(str(subintosub['TimeStamp']))
                    startingtime = startingtime + half_delay
            else:
                for subinto in timer_at_first:
                    startingtime = dateutil.parser.parse(str(subinto['TimeStamp']))
            #
            mergingtime = startingtime + delayActivation
            while 1:
                try:
                    if mergingtime < ServerTime:
                        # High Работа с глобальными переменными. Переприсвоится дальше.
                        endingtime = startingtime + delayActivation
                        #
                        pair_matcher = db[exchname].find({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                                         {'$gte': startingtime, '$lt': endingtime}})
                        sell_data = 0
                        sold_data = 0
                        buy_data = 0
                        bought_data = 0
                        for trdinner in pair_matcher:
                            if trdinner['OrderType'] == 'SELL':
                                sell_data += trdinner['Quantity']
                                sold_data += trdinner['Price']
                            else:
                                buy_data += trdinner['Quantity']
                                bought_data += trdinner['Price']
                        temp_dict_sell = {'PairName': secinner, 'Quantity': sell_data,
                                          'OrderType': 'SELL', 'Price': sold_data,
                                          'TimeStamp': startingtime + half_delay, 'Aggregated': True}
                        temp_dict_buy = {'PairName': secinner, 'Quantity': sell_data,
                                         'OrderType': 'BUY', 'Price': bought_data,
                                         'TimeStamp': startingtime + half_delay, 'Aggregated': True}
                        db[exchname].insert(temp_dict_sell)
                        db[exchname].insert(temp_dict_buy)
                        db[exchname].update({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                            {'$gte': startingtime, '$lt': endingtime}}, {'$set': {'Mod': True}}, multi=True)
                        # Конец работы с циклом, переход на следующие 5 минут времени
                        startingtime = startingtime + delayActivation
                        mergingtime = mergingtime + delayActivation
                    else:
                        break
                except:
                    logging.error(u'VolumeAgg')
        logging.info(u'Check' + exchname + u'collection')


def Tickaggregation(ServerTime):
    import pymongo
    logging.info(u'..TickAggregation started at..' + str(ServerTime))
    global tick, endingtime, startingtime, TimeStamp, PairName
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    exchlist = ['BittrexTick', 'LCoinTick']
    for inner in range(0, len(exchlist)):
        exchname = exchlist[inner]
        print(exchname)
        pairlist = db[exchname].distinct('PairName')
        logging.info(u'Going through..' + exchname)
        #
        for secinner in pairlist:
            # All Matches in DB
            delayActivation = timedelta(minutes=5)
            half_delay = timedelta(minutes=2, seconds=30)
            # Starting time magic
            timer_at_first = db[exchname].find({'PairName': secinner, 'Mod': False}, {'TimeStamp': True}).limit(1)
            #
            enter_counter = db[exchname].find({'PairName': secinner, 'Aggregated': True},
                                              {'TimeStamp': True}).count()
            time_after_aggregation = db[exchname].find({'PairName': secinner, 'Aggregated': True},
                                                       {'TimeStamp': True})\
                .sort('TimeStamp', pymongo.DESCENDING).limit(1)
            if enter_counter > 0:
                for subintosub in time_after_aggregation:
                    startingtime = dateutil.parser.parse(str(subintosub['TimeStamp']))
                    startingtime = startingtime + half_delay
            else:
                for subinto in timer_at_first:
                    startingtime = dateutil.parser.parse(str(subinto['TimeStamp']))
            #
            mergingtime = startingtime + delayActivation

            while 1:
                try:

                    tick = 0
                    if mergingtime < ServerTime:
                        #
                        endingtime = startingtime + delayActivation
                        #
                        pair_matcher = db[exchname].find({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                                         {'$gte': startingtime, '$lt': endingtime}})

                        for trdinner in pair_matcher:
                            if trdinner['Tick'] > tick:
                                tick = trdinner['Tick']
                        temp_dict = {'PairName': secinner, 'Tick': tick,
                                     'TimeStamp': startingtime + half_delay, 'Aggregated': True}
                        db[exchname].insert(temp_dict)
                        db[exchname].update({'PairName': secinner, 'Mod': False, 'TimeStamp':
                            {'$gte': startingtime, '$lt': endingtime}}, {'$set': {'Mod': True}}, multi=True)
                        # Конец работы с циклом, переход на следующие 5 минут времени
                        startingtime = startingtime + delayActivation
                        mergingtime = mergingtime + delayActivation
                    else:
                        break
                except:
                    logging.error(u'Tickagg')
        logging.info(u'Check' + exchname + u'collection')


def arbitration_aggregate():
    import pymongo
    logging.info(u'arbitration reset')
    global tick, timestamp, pair_name
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    exchlist = ['BittrexTick', 'LCoinTick']
    for inner in range(0, len(exchlist)):
        exchname = exchlist[inner]
        pairlist = db[exchname].distinct('PairName')
        logging.info(u'Going through..' + exchname)
        #
        for secinner in pairlist:
            slice = db[exchname].find({'PairName': secinner, 'Aggregated': True}) \
                .sort('TimeStamp', pymongo.ASCENDING).limit(2)
            i = 0
            prev = 0
            for trdinner in slice:
                if (i == 0):
                    prev = trdinner['Tick']
                elif (i == 1):
                    ref = ((trdinner['Tick']-prev)/prev)*100
                    if (ref > 0):
                        tdict = {'Exch': exchname, 'PairName': secinner, 'Tick': trdinner['Tick'], 'Chg': 'U'}
                    elif (ref < 0):
                        tdict = {'Exch': exchname, 'PairName': secinner, 'Tick': trdinner['Tick'], 'Chg': 'D'}
                    else:
                        tdict = {'Exch': exchname, 'PairName': secinner, 'Tick': trdinner['Tick'], 'Chg': 'N'}
                    db.temporaryTick.insert(tdict)
                i = i + 1