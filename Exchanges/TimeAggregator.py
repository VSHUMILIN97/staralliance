from datetime import datetime
import time
from mongo_db_connection import MongoDBConnection
import dateutil.parser
from datetime import datetime, tzinfo, timedelta
from django.utils import timezone, datetime_safe
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)





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
