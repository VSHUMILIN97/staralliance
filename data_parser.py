from Exchanges.ExchangeAPI.bittrexAPI import api_get_getmarketsummaries, api_get_getmarkethistory, api_get_getticker
from Exchanges.ExchangeAPI.liquiAPI import liqui_ticker
from Exchanges.ExchangeAPI.poloniexAPI import poloniex_ticker
from Exchanges.ExchangeAPI.binanceAPI import binance_ticker
from Exchanges.ExchangeAPI.gatecoinAPI import gatecoin_ticker
from Exchanges.ExchangeAPI.livecoinAPI import livecoin_ticker, livecoin_ticker_all_info
from Exchanges.ExchangeAPI.bleutradeAPI import bleutrade_ticker
from Exchanges.ExchangeAPI.ExmoAPI import exmo_ticker, exmo_charts_data, exmo_volume_data
from Exchanges.ExchangeAPI.KucoinAPI import kucoin_ticker
from Exchanges.ExchangeAPI.KrakenAPI import kraken_ticker
from Exchanges.ExchangeAPI.BitfinexAPI import bitfinex_ticker
from Exchanges.ExchangeAPI.HitBTC import hitbtc_ticker
from Exchanges.data_model import ExchangeModel
import time
from mongo_db_connection import MongoDBConnection
import asyncio
from threading import Thread
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


# Works with async to prevent interrupting main thread.
async def data_parse():
    #
    while 1:
        try:
            # Checking for the initial time
            sttime = time.time()
            # Supportive try-catch block. Focused on clearing python and MongoDB resources
            try:
                if ExchangeModel.whole_data:
                    ExchangeModel.pair_clearer()
                    b = MongoDBConnection().start_db()
                    db = b.PiedPiperStock
                    try:
                        db.PoorArb.drop()
                        db.Arbnames.drop()
                    except OSError:
                        logging.warning(u'No collections to drop\nBreakpoint skipped')
                    # Inserting data after dropping DB.
                    db.PoorArb.insert({'Value': ExchangeModel.whole_data})
                    db.Arbnames.insert({'Value': ExchangeModel.cleared_data})
                    b.close()
                    MongoDBConnection().stop_connect()
                    ExchangeModel.cleared_data.clear()
                    ExchangeModel.whole_data.clear()
                    ExchangeModel.support_data.clear()
                # Multithreading ExchangeAPI.
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
                t15 = Thread(target=kraken_ticker)
                t16 = Thread(target=bitfinex_ticker)
                t17 = Thread(target=hitbtc_ticker)
                # Logging purposes.
                """logging.info('t2 alive - ' + str(t2.is_alive()) +
                             ', t3 alive - ' + str(t3.is_alive()) + ', t4 alive - ' + str(t4.is_alive()) +
                             ', t6 alive - ' + str(t6.is_alive()) + ', t7 alive - ' + str(t7.is_alive()) +
                             ', t8 alive - ' + str(t8.is_alive()) + ', t9 alive - ' + str(t9.is_alive()) +
                             ', t10 alive - ' + str(t10.is_alive()) + ', t11 alive - ' + str(t11.is_alive()) +
                             ', t12 alive - ' + str(t12.is_alive()) + ', t13 alive - ' + str(t13.is_alive()) +
                             ', t14 alive - ' + str(t14.is_alive()) + ', t15 alive - ' + str(t15.is_alive()) +
                             ', t16 alive - ' + str(t16.is_alive()) + ', t17 alive - ' + str(t17.is_alive()))"""
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
                t15._stop()
                t16._stop()
                t17._stop()
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
                t15.setDaemon(True)
                t16.setDaemon(True)
                t17.setDaemon(True)
                t16.start()
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
                t15.start()
                t17.start()
            except ConnectionError:
                logging.error(u'Data were not recieved')
                continue
            # Checking for the ending time
            endtime = time.time()
            mergetime = endtime - sttime
            # Creating a co-routine. Sending a subprocess to sleep.
            await asyncio.sleep(25 - mergetime)
        except OSError:
            logging.error(u'Async event failed to perform\nApp will be stopped by crash')

# Initialise infinite data parse from public API.
loop = asyncio.get_event_loop()
loop.run_until_complete(data_parse())
loop.run_forever()
