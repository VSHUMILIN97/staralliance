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
            if slice.count() >= 2:
                if slice[1]['Tick'] < slice[0]['Tick']:
                    tdict = {'Exch': exchname.replace('Tick', ''), 'PairName': secinner,
                             'Tick': slice[0]['Tick'], 'Chg': 'U'}
                elif slice[1]['Tick'] > slice[0]['Tick']:
                    tdict = {'Exch': exchname.replace('Tick', ''), 'PairName': secinner,
                             'Tick': slice[0]['Tick'], 'Chg': 'D'}
                else:
                    tdict = {'Exch': exchname.replace('Tick', ''), 'PairName': secinner,
                             'Tick': slice[0]['Tick'], 'Chg': 'N'}
                db.temporaryTick.insert(tdict)
