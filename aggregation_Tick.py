from mongo_db_connection import MongoDBConnection
import dateutil.parser
from datetime import timedelta
import logging
import datetime
import time
import asyncio

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


def Tickaggregation(ServerTime):
    import pymongo
    logging.info(u'TickAggregation started at..' + str(ServerTime))
    global tick, endingtime, startingtime, TimeStamp, PairName, hammertime
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    exchlist = ['BittrexTick', 'LiveCoinTick', 'GatecoinTick', 'LiquiTick', 'BleutradeTick', 'PoloniexTick',
                'BinanceTick', 'ExmoTick']
    for inner in range(0, len(exchlist)):
        exchname = exchlist[inner]
        pairlist = db[exchname].distinct('PairName')
        #
        for secinner in pairlist:
            # All Matches in DB
            delayActivation = timedelta(seconds=30)
            half_delay = timedelta(seconds=15)
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
            #
            try:
                hammertime = dateutil.parser.parse(str(time_after_aggregation[0]['TimeStamp']))
            except():
                logging.info(u'Missing hammertime at OHLC_VOL')
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
                        tick = 0  # 1
                        #
                        endingtime = startingtime + delayActivation
                        #
                        pair_matcher = db[exchname].find({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                                         {'$gte': startingtime, '$lt': endingtime}})
                        if pair_matcher.count() == 0:
                            logging.critical('MISSING DATA IN - ' + exchname + ', ' + secinner)
                        #
                        for trdinner in pair_matcher:
                            if trdinner['Tick'] >= tick:
                                tick = trdinner['Tick']
                        temp_dict = {'PairName': secinner, 'Tick': tick,
                                     'TimeStamp': startingtime + half_delay, 'Aggregated': True}
                        db[exchname].insert(temp_dict)
                        db[exchname].update({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                            {'$gte': startingtime, '$lt': endingtime}},
                                            {'$set': {'Mod': True}}, multi=True)
                        # Конец работы с циклом, переход на следующие 30 секунд времени
                        startingtime = startingtime + delayActivation
                        mergingtime = mergingtime + delayActivation
                        pair_matcher.close()
                    else:
                        startingtime = startingtime + delayActivation
                        mergingtime = mergingtime + delayActivation
                        break
                except:
                    logging.error(u'Tickagg')
            timer_at_first.close()
            time_after_aggregation.close()
        logging.info(u'Check' + exchname + u'collection')


async def loop_aggr_tick():
    while 1:
        srv_time = datetime.datetime.utcnow()
        logging.info(u'AggregationTick started')
        sttime = time.time()
        Tickaggregation(srv_time)
        logging.info(u'AggregationTick confirmed')
        endtime = time.time()
        mergetime = endtime - sttime
        await asyncio.sleep(30 - mergetime)

loop = asyncio.get_event_loop()
loop.run_until_complete(loop_aggr_tick())
loop.run_forever()
