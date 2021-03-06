from mongo_db_connection import MongoDBConnection
import dateutil.parser
from datetime import timedelta
import logging
import datetime
import time
import asyncio

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename='/var/log/cryptopiper/aggregation_Tick.log')

"""
#
#
NOT IN WORK. CLOSE THIS SCRIPT
#
#
"""


def Tickaggregation(ServerTime):
    import pymongo
    logging.info(u'TickAggregation started at..' + str(ServerTime))
    global tick, endingtime, startingtime, TimeStamp, PairName, hammertime,\
        pair_matcher, timer_at_first, time_after_aggregation
    b = MongoDBConnection().start_local()
    db = b.PiedPiperStock
    exchlist = ['BittrexTick', 'LiveCoinTick', 'GatecoinTick', 'LiquiTick', 'BleutradeTick', 'PoloniexTick',
                'BinanceTick', 'ExmoTick']
    for inner in range(0, len(exchlist)):
        exchname = exchlist[inner]
        pairlist = db[exchname].distinct('PairName')
        #
        for secinner in pairlist:
            # All Matches in DB
            delayActivation = timedelta(seconds=300)
            half_delay = timedelta(seconds=150)
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
                        tick = 0  # 1
                        #
                        endingtime = mergingtime
                        #
                        pair_matcher = db[exchname].find({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                                         {'$gte': startingtime, '$lt': endingtime}})
                        for trdinner in pair_matcher:
                            if trdinner['Tick'] >= tick:
                                tick = trdinner['Tick']
                        temp_dict = {'PairName': secinner, 'Tick': tick,
                                     'TimeStamp': endingtime - half_delay, 'Aggregated': True}
                        db[exchname].insert(temp_dict)
                        db[exchname].update({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                            {'$gte': startingtime, '$lt': endingtime}},
                                            {'$set': {'Mod': True}}, multi=True)
                        # Конец работы с циклом, переход на следующие 30 секунд времени
                        startingtime = startingtime + delayActivation
                        mergingtime = mergingtime + delayActivation
                        pair_matcher.close()
                    else:
                        break
                except():
                    logging.error(u'Tickagg')
            timer_at_first.close()
            time_after_aggregation.close()
        logging.info(u'Check' + exchname + u'collection')
        #
    MongoDBConnection().stop_connect()


def indexator():
    logging.info(u'IndexatorVol started')
    global sell_data, endingtime, startingtime, buy_data, TimeStamp, PairName, sold_data,\
        bought_data, pairlist, timer_at_first, time_after_aggregation, pair_matcher
    b = MongoDBConnection().start_local()
    db = b.PiedPiperStock
    exchlist = ['BittrexTick', 'LiveCoinTick', 'GatecoinTick', 'LiquiTick', 'BleutradeTick', 'PoloniexTick',
                'BinanceTick', 'ExmoTick']
    indexes = ['TimeStamp', 'Mod', 'Aggregated']
    from pymongo import IndexModel, ASCENDING
    for inner in range(0, len(exchlist)):
        exchname = exchlist[inner]
        for secinner in range(0, len(indexes)):
            index = IndexModel([(indexes[secinner], ASCENDING)])
            db[exchname].create_indexes([index])
    logging.info(u'Indexator completed his work')
    MongoDBConnection().stop_connect()


async def loop_aggr_tick():
    indexator()
    time.sleep(5)
    while 1:
        sttm = time.time()
        srv_time = datetime.datetime.utcnow()
        logging.info(u'AggregationTick started')
        Tickaggregation(srv_time)
        logging.info(u'AggregationTick confirmed')
        mttm = 30 - (time.time() - sttm)
        await asyncio.sleep(mttm)

loop = asyncio.get_event_loop()
loop.run_until_complete(loop_aggr_tick())
loop.run_forever()
