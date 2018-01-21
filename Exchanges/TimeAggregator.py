from datetime import datetime
import time
from mongo_db_connection import MongoDBConnection
import dateutil.parser
from datetime import datetime, tzinfo, timedelta
from django.utils import timezone, datetime_safe
import logging

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
            for subintosub in time_after_aggregation:
                hammertime = dateutil.parser.parse(str(subintosub['TimeStamp']))
            if hammertime != ServerTime and hammertime + half_delay < ServerTime:
                startingtime = ServerTime - delayActivation - microdelta
            elif enter_counter > 0:
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


def arbitration_aggregate():
    import pymongo
    logging.info(u'arbitration reset')
    global tick, timestamp, pair_name
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock

    exchlist = ['BittrexTick', 'LiveCoinTick', 'GatecoinTick', 'LiquiTick', 'BleutradeTick', 'PoloniexTick',
                'BinanceTick', 'ExmoTick']
    #
    for inner in range(0, len(exchlist)):
        exchname = exchlist[inner]
        pairlist = db[exchname].distinct('PairName')
        #
        for secinner in pairlist:
            slice = db[exchname].find({'PairName': secinner, 'Aggregated': True}) \
                .sort('TimeStamp', pymongo.DESCENDING).limit(2)
            i = 0
            future_tick = 0
            for trdinner in slice:
                if (i == 0):
                    future_tick = trdinner['Tick']
                elif (i == 1):
                    ref = ((trdinner['Tick']-future_tick)/future_tick)*100
                    if (ref > 0):
                        tdict = {'Exch': exchname.replace('Tick', ''), 'PairName': secinner,
                                 'Tick': future_tick, 'Chg': 'D'}
                    elif (ref < 0):
                        tdict = {'Exch': exchname.replace('Tick', ''), 'PairName': secinner,
                                 'Tick': future_tick, 'Chg': 'U'}
                    else:
                        tdict = {'Exch': exchname.replace('Tick', ''), 'PairName': secinner,
                                 'Tick': future_tick, 'Chg': 'N'}
                    db.temporaryTick.insert(tdict)
                i = i + 1
