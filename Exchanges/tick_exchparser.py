import datetime
from Exchanges.BittrexObjCreate import api_get_getmarkethistory, api_get_getticker,\
     api_get_getmarketsummaries, livecoin_ticker
import random
from .TimeAggregator import OHLCaggregation, Volumeaggregation, Tickaggregation
import time
from threading import Thread
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


class ThreadingT(Thread):
    def run(self):
        logging.info(u'Data requested')
        self.random_seed()

    def random_seed(self):
        # Методом проб и ошибок мы выяснили, что потоки нужно останавливать прямо внутри цикла, благо
        # питсон позволяет/ Безопасность из говна и палок, как и код. Доработать со временем!
        while 1:
            try:
                # Частота опроса биржи по их Public API. Легкая защита от отключения данных
                timeTemp = random.uniform(52, 58)  # Значения можно менять
                logging.info(u'Delay before request..' + str(timeTemp))
                #
                try:
                    t1 = Thread(target=api_get_getmarketsummaries)
                    t2 = Thread(target=api_get_getmarkethistory)
                    t3 = Thread(target=api_get_getticker)
                    t4 = Thread(target=livecoin_ticker())
                    t1._stop()
                    t2._stop()
                    t3._stop()
                    t4._stop()
                    t1.setDaemon(True)
                    t2.setDaemon(True)
                    t3.setDaemon(True)
                    t4.setDaemon(True)
                    t1.start()
                    t2.start()
                    t3.start()
                    t4.start()
                    t1.join()
                    t2.join()
                    t3.join()
                    t4.join()
                    Tickaggregation(datetime.datetime.utcnow())
                except():
                    logging.error(u'Data were not recieved')
                time.sleep(timeTemp)
            except():
                logging.error('Threads bump')


"""def aggregation_trigger():
    while 1:
        logging.info(u'Aggregations started')
        try:
            threadf = Thread(target=OHLCaggregation(datetime.datetime.utcnow()))
            thread2f = Thread(target=Volumeaggregation(datetime.datetime.utcnow()))
            thread3f = Thread(target=Tickaggregation(datetime.datetime.utcnow()))
            threadf._stop()
            thread2f._stop()
            thread3f._stop()
            threadf.setDaemon(True)
            thread2f.setDaemon(True)
            thread3f.setDaemon(True)
            threadf.start()
            thread2f.start()
            thread3f.start()
        except():
            logging.error(u'Aggregation had not been finished')
        logging.info(u'Aggregation confirmed')
        time.sleep(300)"""
