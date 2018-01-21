import datetime
from .ExchangeAPI.bittrexAPI import api_get_getmarketsummaries, api_get_getmarkethistory, api_get_getticker
from .ExchangeAPI.liquiAPI import liqui_ticker
from .ExchangeAPI.poloniexAPI import poloniex_ticker
from .ExchangeAPI.binanceAPI import binance_ticker
from .ExchangeAPI.gatecoinAPI import gatecoin_ticker
from .ExchangeAPI.livecoinAPI import livecoin_ticker, livecoin_ticker_all_info
from .ExchangeAPI.bleutradeAPI import bleutrade_ticker
from .ExchangeAPI.ExmoAPI import exmo_ticker
import random
from .TimeAggregator import Tickaggregation
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
                # Lock стоит для графиков на время работы с арбитражом.
                timeTemp = random.uniform(13.1, 15)  # Значения можно менять
                logging.info(u'Delay before request..' + str(timeTemp))
                #
                try:
                    t1 = Thread(target=api_get_getmarketsummaries)
                    t2 = Thread(target=api_get_getmarkethistory)
                    t3 = Thread(target=api_get_getticker)
                    t4 = Thread(target=livecoin_ticker)
                    #t5 = Thread(target=livecoin_ticker_all_info)
                    t6 = Thread(target=gatecoin_ticker)
                    t7 = Thread(target=liqui_ticker)
                    t8 = Thread(target=bleutrade_ticker)
                    t9 = Thread(target=poloniex_ticker)
                    t10 = Thread(target=binance_ticker)
                    t11 = Thread(target=exmo_ticker)
                    t1._stop()
                    t2._stop()
                    logging.info('t1 alive - ' + str(t1.is_alive()) + ', t2 alive - ' + str(t2.is_alive()) +
                                 ', t3 alive - ' + str(t3.is_alive()) + ', t4 alive - ' + str(t4.is_alive()) +
                                 ', t6 alive - ' + str(t6.is_alive()) + ', t7 alive - ' + str(t7.is_alive()) +
                                 ', t8 alive - ' + str(t8.is_alive()) + ', t9 alive - ' + str(t9.is_alive()) +
                                 ', t10 alive - ' + str(t10.is_alive())+ ', t11 alive -' + str(t11.is_alive()))
                    t3._stop()
                    t4._stop()
                    #t5._stop()
                    t6._stop()
                    t7._stop()
                    t8._stop()
                    t9._stop()
                    t10._stop()
                    t11._stop()
                    t1.setDaemon(True)
                    t2.setDaemon(True)
                    t3.setDaemon(True)
                    t4.setDaemon(True)
                    #t5.setDaemon(True)
                    t6.setDaemon(True)
                    t7.setDaemon(True)
                    t8.setDaemon(True)
                    t9.setDaemon(True)
                    t10.setDaemon(True)
                    t11.setDaemon(True)
                    t1.start()
                    t2.start()
                    t3.start()
                    t4.start()
                    #t5.start()
                    t6.start()
                    t7.start()
                    t8.start()
                    t9.start()
                    t10.start()
                    t11.start()
                except():
                    logging.error(u'Data were not recieved')
                time.sleep(timeTemp)
            except():
                logging.error('Threads bump')


class ThreadingAT(Thread):
    def run(self):
        logging.info(u'Aggregation of tick is requested')
        self.aggregation_trigger()

    def aggregation_trigger(self):
        time.sleep(30)
        while 1:
            logging.info(u'AggregationTick started')
            try:
                stime = datetime.datetime.utcnow()
                td_tick = Thread(target=Tickaggregation(stime))
                td_tick._stop()
                td_tick.setDaemon(True)
                td_tick.start()
            except():
                logging.error(u'AggregationTick had not been finished')
            logging.info(u'AggregationTick confirmed')
            time.sleep(30)
