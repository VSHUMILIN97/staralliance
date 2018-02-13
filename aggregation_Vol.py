from mongo_db_connection import MongoDBConnection
import dateutil.parser
from datetime import timedelta
import logging
import datetime
import asyncio
import time

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename='/var/log/cryptopiper/aggregation_Vol.log')


def Volumeaggregation(ServerTime):
    import pymongo
    logging.info(u'..VolumeAggregation started at..' + str(ServerTime))
    global sell_data, endingtime, startingtime, buy_data, TimeStamp, PairName, sold_data,\
        bought_data, pairlist, timer_at_first, time_after_aggregation, pair_matcher
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    exchlist = ['BittrexMHist', 'ExmoMHist']
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
            time_after_aggregation = db[exchname].find({'PairName': secinner, 'Aggregated': True},
                                                       {'TimeStamp': True})\
                .sort('TimeStamp', pymongo.DESCENDING).limit(1)
            #
            if time_after_aggregation.count() > 0:
                startingtime = dateutil.parser.parse(str(time_after_aggregation[0]['TimeStamp']))
                startingtime = startingtime + half_delay
            else:
                startingtime = dateutil.parser.parse(str(timer_at_first[0]['TimeStamp']))
            #
            mergingtime = startingtime + delayActivation
            if mergingtime + delayActivation*2 < ServerTime:
                mergingtime = ServerTime - delayActivation - microdelta
            while 1:
                try:
                    if mergingtime < ServerTime:
                        # High Работа с глобальными переменными. Переприсвоится дальше.
                        endingtime = mergingtime
                        #
                        pair_matcher = db[exchname].find({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                                         {'$gte': startingtime, '$lt': endingtime}})
                        sell_data = 0
                        buy_data = 0
                        for item in pair_matcher:
                            if item['OrderType'] == 'SELL':
                                sell_data += item['Quantity']
                            else:
                                buy_data += item['Quantity']
                        #
                        if sell_data and buy_data == 0:
                            startingtime = startingtime + delayActivation
                            mergingtime = mergingtime + delayActivation
                            pair_matcher.close()
                            continue
                        temp_dict_sell = {'PairName': secinner, 'Quantity': sell_data,
                                          'OrderType': 'SELL', 'TimeStamp': endingtime - half_delay, 'Aggregated': True}
                        temp_dict_buy = {'PairName': secinner, 'Quantity': buy_data,
                                         'OrderType': 'BUY', 'TimeStamp': endingtime - half_delay, 'Aggregated': True}
                        db[exchname].insert(temp_dict_sell)
                        db[exchname].insert(temp_dict_buy)
                        db[exchname].update({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                            {'$gte': startingtime, '$lt': endingtime}},
                                            {'$set': {'Mod': True}}, multi=True)
                        # Конец работы с циклом, переход на следующие 5 минут времени
                        startingtime = startingtime + delayActivation
                        mergingtime = mergingtime + delayActivation
                        pair_matcher.close()
                    else:
                        break
                except():
                    logging.error(u'VolumeAgg')
            time_after_aggregation.close()
            timer_at_first.close()
        logging.info(u'Check' + exchname + u'collection')
    MongoDBConnection().stop_connect()


def indexator():
    logging.info(u'IndexatorVol started')
    global sell_data, endingtime, startingtime, buy_data, TimeStamp, PairName, sold_data, bought_data, pairlist, timer_at_first, time_after_aggregation, pair_matcher
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    exchlist = ['BittrexMHist', 'ExmoMHist']
    indexes = ['TimeStamp', 'Mod', 'Aggregated']
    from pymongo import IndexModel, ASCENDING
    for inner in range(0, len(exchlist)):
        exchname = exchlist[inner]
        for secinner in range(0, len(indexes)):
            index = IndexModel([(indexes[secinner], ASCENDING)])
            db[exchname].create_indexes([index])
    logging.info(u'Indexator completed his work')
    MongoDBConnection().stop_connect()


async def loop_aggr_Vol():
    indexator()
    time.sleep(5)
    while 1:
        sttm = time.time()
        srv_time = datetime.datetime.utcnow()
        logging.info(u'AggregationOHLCVol started')
        Volumeaggregation(srv_time)
        logging.info(u'AggregationOHLCVol confirmed')
        mttm = 300 - (time.time() - sttm)
        await asyncio.sleep(mttm)

loop = asyncio.get_event_loop()
loop.run_until_complete(loop_aggr_Vol())
loop.run_forever()
