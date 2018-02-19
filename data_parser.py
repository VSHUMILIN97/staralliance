from Exchanges.ExchangeAPI.bittrexAPI import api_get_getmarketsummaries, api_get_getmarkethistory, api_get_getticker
from Exchanges.ExchangeAPI.liquiAPI import liqui_ticker
from Exchanges.ExchangeAPI.poloniexAPI import poloniex_ticker
from Exchanges.ExchangeAPI.binanceAPI import binance_ticker
from Exchanges.ExchangeAPI.gatecoinAPI import gatecoin_ticker
from Exchanges.ExchangeAPI.livecoinAPI import livecoin_ticker, livecoin_ticker_all_info
from Exchanges.ExchangeAPI.bleutradeAPI import bleutrade_ticker
from Exchanges.ExchangeAPI.ExmoAPI import exmo_ticker, exmo_charts_data, exmo_volume_data
from Exchanges.ExchangeAPI.KucoinAPI import kucoin_ticker
from Exchanges.data_model import EMWrapper, ExchangeModel
import random
import time
from mongo_db_connection import MongoDBConnection
import asyncio
from threading import Thread
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


async def data_parse():
    # Методом проб и ошибок мы выяснили, что потоки нужно останавливать прямо внутри цикла, благо
    # питсон позволяет/ Безопасность из говна и палок, как и код. Доработать со временем!
    while 1:
        try:
            sttime = time.time()
            # Частота опроса биржи по их Public API. Легкая защита от отключения данных
            # Lock стоит для графиков на время работы с арбитражом.
            # Значения можно менять
            #
            try:
                if ExchangeModel.whole_data:
                    ExchangeModel.pair_clearer()
                    b = MongoDBConnection().start_db()
                    db = b.PiedPiperStock
                    try:
                        db.PoorArb.drop()
                        db.Arbnames.drop()
                    except():
                        None
                    db.PoorArb.insert({'Value': ExchangeModel.whole_data})
                    db.Arbnames.insert({'Value': ExchangeModel.cleared_data})
                    b.close()
                    MongoDBConnection().stop_connect()
                    ExchangeModel.cleared_data.clear()
                    ExchangeModel.whole_data.clear()
                    ExchangeModel.support_data.clear()
                t1 = Thread(target=api_get_getmarketsummaries)
                t2 = Thread(target=api_get_getmarkethistory)
                t3 = Thread(target=api_get_getticker)
                t4 = Thread(target=livecoin_ticker)
                # t5 = Thread(target=livecoin_ticker_all_info)
                t6 = Thread(target=gatecoin_ticker)
                t7 = Thread(target=liqui_ticker)
                t8 = Thread(target=bleutrade_ticker)
                t9 = Thread(target=poloniex_ticker)
                t10 = Thread(target=binance_ticker)
                t11 = Thread(target=exmo_ticker)
                t12 = Thread(target=exmo_volume_data)
                t13 = Thread(target=exmo_charts_data)
                t14 = Thread(target=kucoin_ticker)
                """logging.info('t2 alive - ' + str(t2.is_alive()) +
                             ', t3 alive - ' + str(t3.is_alive()) + ', t4 alive - ' + str(t4.is_alive()) +
                             ', t6 alive - ' + str(t6.is_alive()) + ', t7 alive - ' + str(t7.is_alive()) +
                             ', t8 alive - ' + str(t8.is_alive()) + ', t9 alive - ' + str(t9.is_alive()) +
                             ', t10 alive - ' + str(t10.is_alive()) + ', t11 alive - ' + str(t11.is_alive()) +
                             ', t12 alive - ' + str(t12.is_alive()) + ', t13 alive - ' + str(t13.is_alive()) +
                             ', t14 alive -' + str(t14.is_alive()))"""
                t1._stop()
                t2._stop()
                t3._stop()
                t4._stop()
                # t5._stop()
                t6._stop()
                t7._stop()
                t8._stop()
                t9._stop()
                t10._stop()
                t11._stop()
                t12._stop()
                t13._stop()
                t14._stop()
                t1.setDaemon(True)
                t2.setDaemon(True)
                t3.setDaemon(True)
                t4.setDaemon(True)
                # t5.setDaemon(True)
                t6.setDaemon(True)
                t7.setDaemon(True)
                t8.setDaemon(True)
                t9.setDaemon(True)
                t10.setDaemon(True)
                t11.setDaemon(True)
                t12.setDaemon(True)
                t13.setDaemon(True)
                t14.setDaemon(True)
                t1.start()
                t2.start()
                t3.start()
                t4.start()
                # t5.start()
                t6.start()
                t7.start()
                t8.start()
                t9.start()
                t10.start()
                t11.start()
                t12.start()
                t13.start()
                t14.start()
            except():
                logging.error(u'Data were not recieved')
            endtime = time.time()
            mergetime = endtime - sttime
            await asyncio.sleep(22 - mergetime)
        except():
            logging.error('Threads bump')

loop = asyncio.get_event_loop()
loop.run_until_complete(data_parse())
loop.run_forever()
