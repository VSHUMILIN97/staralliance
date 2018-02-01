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
                        highest_value = 0
                        lowest_value = 9999999
                        endingtime = mergingtime
                        #
                        open_val_dict = db[exchname].find({'PairName': secinner, 'Aggregated': True},
                                                          {'Close': True})\
                            .sort('TimeStamp', pymongo.DESCENDING).limit(1)

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
                                open_value = open_val_dict[0]['Close']
                            else:
                                nxt_crsr = db[exchname].find(
                                    {'PairName': secinner, 'Mod': False, 'TimeStamp':
                                        {'$gte': startingtime, '$lt': endingtime}},
                                    {'Price': True}) \
                                    .sort('TimeStamp', pymongo.ASCENDING).limit(1)
                                open_value = nxt_crsr[0]['Price']
                            # PrevDay
                            if close_val_dict.count() > 0:
                                close_value = close_val_dict[0]['Price']
                            #
                        except():
                            logging.critical(u'NO OPEN AND CLOSE DATA RECEIVED')
                        try:
                            close_value
                        except NameError:
                            logging.critical(u'Aggregation cycle dropped!!!')
                            break
                        for trdinner in pair_matcher:
                            if trdinner['Price'] > highest_value:
                                highest_value = trdinner['Price']
                            if trdinner['Price'] < lowest_value:
                                lowest_value = trdinner['Price']
                            if lowest_value == 9999999:
                                lowest_value = close_value
                        tempdict = {'PairName': secinner, 'High': highest_value,
                                    'Low': lowest_value, 'TimeStamp': endingtime - half_delay, 'Close': close_value,
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


async def loop_aggr_OHLC():
    while 1:
        srv_time = datetime.datetime.utcnow()
        logging.info(u'AggregationOHLC started')
        OHLCaggregation(srv_time)
        logging.info(u'AggregationOHLC confirmed')
        await asyncio.sleep(300)

loop = asyncio.get_event_loop()
loop.run_until_complete(loop_aggr_OHLC())
loop.run_forever()
