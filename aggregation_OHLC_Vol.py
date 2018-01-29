from mongo_db_connection import MongoDBConnection
import dateutil.parser
from datetime import timedelta
import logging
import datetime
import asyncio
import time

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


def OHLCaggregation(ServerTime):
    import pymongo
    global highest_value, endingtime, startingtime, close_value, open_value
    global lowest_value
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
            microdelta = timedelta(milliseconds=1)
            # Starting time magic
            timer_at_first = db[exchname].find({'PairName': secinner, 'Mod': False}, {'TimeStamp': True}).limit(1)
            #
            enter_counter = db[exchname].find({'PairName': secinner, 'Aggregated': True},
                                              {'TimeStamp': True}).count()
            time_after_aggregation = db[exchname].find({'PairName': secinner, 'Aggregated': True},
                                                       {'TimeStamp': True})\
                .sort('TimeStamp', pymongo.DESCENDING).limit(1)
            hammertime = ServerTime
            try:
                if time_after_aggregation.count() > 0:
                    hammertime = dateutil.parser.parse(str(time_after_aggregation[0]['TimeStamp']))
            except():
                logging.info(u'missing hammertime at OHLC_VOL')
            if hammertime != ServerTime and hammertime + half_delay < ServerTime:
                startingtime = ServerTime - delayActivation - microdelta
            elif enter_counter > 0:
                startingtime = dateutil.parser.parse(str(time_after_aggregation[0]['TimeStamp']))
                startingtime = startingtime + half_delay
            else:
                startingtime = dateutil.parser.parse(str(timer_at_first[0]['TimeStamp']))
            #
            mergingtime = startingtime + delayActivation
            while 1:
                try:
                    if mergingtime < ServerTime:
                        # High Работа с глобальными переменными. Переприсвоится дальше.
                        highest_value = 0
                        lowest_value = 9999999
                        endingtime = mergingtime
                        # Low Записываем значение из одномерного словаря (Это можно отрефакторить - WELCOME!)
                        open_val_dict = db[exchname].find({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                                          {'$gte': startingtime, '$lt': endingtime}},
                                                          {'Price': True})\
                            .sort('TimeStamp', pymongo.ASCENDING).limit(1)

                        # Last Пишем первый объект из коллекции. Так и не разобрались с полем.
                        # Поиск по паре, полю Mod - Modified/ TimeStamp в разрезе от startingtime до endingtime
                        close_val_dict = db[exchname].find({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                                           {'$gte': startingtime, '$lt': endingtime}},
                                                           {'Price': True})\
                            .sort('TimeStamp', pymongo.DESCENDING).limit(1)
                        #
                        pair_matcher = db[exchname].find({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                                         {'$gte': startingtime, '$lt': endingtime}})
                        # Last
                        try:
                            if open_val_dict.count() > 0:
                                open_value = open_val_dict[0]['Price']
                            # PrevDay
                            if close_val_dict.count() > 0:
                                close_value = close_val_dict[0]['Price']
                            #
                        except():
                            logging.critical(u'NO OPEN AND CLOSE DATA RECEIVED')
                        if open_val_dict.count() == 0 and close_val_dict.count() == 0 and pair_matcher.count() == 0:
                            break
                        for trdinner in pair_matcher:
                            if trdinner['Price'] > highest_value:
                                highest_value = trdinner['Price']
                            if trdinner['Price'] < lowest_value:
                                lowest_value = trdinner['Price']
                            if lowest_value == 9999999:
                                lowest_value = close_value
                        tempdict = {'PairName': secinner, 'High': highest_value,
                                    'Low': lowest_value, 'TimeStamp': startingtime - half_delay, 'Close': close_value,
                                    'Open': open_value, 'Aggregated': True}
                        db[exchname].insert(tempdict)
                        db[exchname].update({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                            {'$gte': startingtime, '$lt': endingtime}}, {'$set': {'Mod': True}},
                                            multi=True)
                        # Конец работы с циклом, переход на следующие 5 минут времени

                        startingtime = startingtime + delayActivation
                        mergingtime = mergingtime + delayActivation
                    else:
                        break
                except():
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
            microdelta = timedelta(milliseconds=1)
            # Starting time magic
            timer_at_first = db[exchname].find({'PairName': secinner, 'Mod': False}, {'TimeStamp': True}).limit(1)
            #
            enter_counter = db[exchname].find({'PairName': secinner, 'Aggregated': True},
                                              {'TimeStamp': True}).count()
            time_after_aggregation = db[exchname].find({'PairName': secinner, 'Aggregated': True},
                                                       {'TimeStamp': True})\
                .sort('TimeStamp', pymongo.DESCENDING).limit(1)
            hammertime = ServerTime
            try:
                hammertime = dateutil.parser.parse(str(time_after_aggregation[0]['TimeStamp']))
            except():
                logging.info(u'missing hammertime at OHLC_VOL')
            if hammertime != ServerTime and hammertime + half_delay < ServerTime:
                startingtime = ServerTime - delayActivation - microdelta
            elif enter_counter > 0:
                startingtime = dateutil.parser.parse(str(time_after_aggregation[0]['TimeStamp']))
                startingtime = startingtime + half_delay
            else:
                startingtime = dateutil.parser.parse(str(timer_at_first[0]['TimeStamp']))
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
                        for item in range(0, pair_matcher.count()):
                            if pair_matcher[item]['OrderType'] == 'SELL':
                                sell_data += pair_matcher[item]['Quantity']
                                sold_data += pair_matcher[item]['Price']
                            else:
                                buy_data += pair_matcher[item]['Quantity']
                                bought_data += pair_matcher[item]['Price']
                        temp_dict_sell = {'PairName': secinner, 'Quantity': sell_data,
                                          'OrderType': 'SELL', 'Price': sold_data,
                                          'TimeStamp': startingtime - half_delay, 'Aggregated': True}
                        temp_dict_buy = {'PairName': secinner, 'Quantity': sell_data,
                                         'OrderType': 'BUY', 'Price': bought_data,
                                         'TimeStamp': startingtime - half_delay, 'Aggregated': True}
                        db[exchname].insert(temp_dict_sell)
                        db[exchname].insert(temp_dict_buy)
                        db[exchname].update({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                            {'$gte': startingtime, '$lt': endingtime}},
                                            {'$set': {'Mod': True}}, multi=True)
                        # Конец работы с циклом, переход на следующие 5 минут времени
                        startingtime = startingtime + delayActivation
                        mergingtime = mergingtime + delayActivation
                    else:
                        break
                except:
                    logging.error(u'VolumeAgg')
        logging.info(u'Check' + exchname + u'collection')


async def loop_aggr_OHLC_Vol():
    while 1:
        srv_time = datetime.datetime.utcnow()
        logging.info(u'AggregationOHLCVol started')
        sttime = time.time()
        OHLCaggregation(srv_time)
        Volumeaggregation(srv_time)
        endtime = time.time()
        mergetime = endtime - sttime
        logging.info(u'AggregationOHLCVol confirmed')
        await asyncio.sleep(300 - mergetime)

loop = asyncio.get_event_loop()
loop.run_until_complete(loop_aggr_OHLC_Vol())
loop.run_forever()
