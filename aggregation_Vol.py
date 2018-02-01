from mongo_db_connection import MongoDBConnection
import dateutil.parser
from datetime import timedelta
import logging
import datetime
import asyncio
import time

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


def Volumeaggregation(ServerTime):
    import pymongo
    logging.info(u'..VolumeAggregation started at..' + str(ServerTime))
    global sell_data, endingtime, startingtime, buy_data, TimeStamp, PairName, sold_data, bought_data
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    exchlist = ['BittrexMHist']
    timeexch = ['Bittrex']
    for inner in range(0, len(exchlist)):
        exchname = exchlist[inner]
        exchtime = timeexch[inner]
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
            while 1:
                try:
                    if mergingtime < ServerTime:
                        # High Работа с глобальными переменными. Переприсвоится дальше.
                        endingtime = mergingtime
                        #
                        pair_matcher = db[exchname].find({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                                         {'$gte': startingtime, '$lt': endingtime}})
                        sell_data = 0
                        sold_data = 0
                        buy_data = 0
                        bought_data = 0
                        for item in pair_matcher:
                            if item['OrderType'] == 'SELL':
                                sell_data += item['Quantity']
                            else:
                                buy_data += item['Quantity']
                        #
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
                    else:
                        break
                except():
                    logging.error(u'VolumeAgg')
        logging.info(u'Check' + exchname + u'collection')


async def loop_aggr_Vol():
    while 1:
        srv_time = datetime.datetime.utcnow()
        logging.info(u'AggregationOHLCVol started')
        Volumeaggregation(srv_time)
        logging.info(u'AggregationOHLCVol confirmed')
        await asyncio.sleep(300)

loop = asyncio.get_event_loop()
loop.run_until_complete(loop_aggr_Vol())
loop.run_forever()
