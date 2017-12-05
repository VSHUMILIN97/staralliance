import datetime

from Exchanges.BittrexObjCreate import api_get_getmarkethistory, api_get_getticker, api_get_getmarketsummaries
import random
from .TimeAggregator import OHLCaggregation, Volumeaggregation, Tickaggregation
import time
from threading import Thread


class ThreadingT(Thread):
    def run(self):
        self.random_seed()

        # Реально работает, но вызывает ошибку если пытаться вызывать методы =) Ошибка выше
        # UPD: Ошибку пофиксил, изабвился от асинхрона.
        # UPD(2):Запускается 1 раз при старте сервера и работает до талого. Фух сцук.
        # С функциями на получение данных работает спокойно. Дополнительных импортов НЕ НАДО.
        # Требует доработки по триггеру агрегатора
        # Вот тут мы узнаем, что база данных блокируется, а по сему велю, сделать LOCK.
        # Хранить часть данных в оперативе - наш кандидат

    def random_seed(self):
        # Методом проб и ошибок мы выяснили, что потоки нужно останавливать прямо внутри цикла, благо
        # питсон позволяет/ Безопасность из говна и палок, как и код. Доработать со временем!
        while 1:
            try:
                # Частота опроса биржи по их Public API. Легкая защита от отключения данных
                timeTemp = random.uniform(52, 58)  # Значения можно менять
                print(timeTemp)
                # Пока что закрыто, так как БД очень сильно засирается.
                try:
                    t1 = Thread(target=api_get_getmarketsummaries)
                    t2 = Thread(target=api_get_getmarkethistory)
                    t3 = Thread(target=api_get_getticker)
                    t1._stop()
                    t2._stop()
                    t3._stop()
                    t1.start()
                    t2.start()
                    t3.start()
                    t1.join()
                    t2.join()
                    t3.join()
                except(Exception):
                    print('Mistake in random_seed')
                time.sleep(timeTemp)
            except:
                print('Overflow error in tick_exchparser')


def aggregation_trigger():
    while 1:
        print('Starting aggregation...'+str(time.time()))
        thread = Thread(target=OHLCaggregation(datetime.datetime.utcnow()))
        thread2 = Thread(target=Volumeaggregation(datetime.datetime.utcnow()))
        thread3 = Thread(target=Tickaggregation(datetime.datetime.utcnow()))
        thread._stop()
        thread2._stop()
        thread3._stop()
        thread.start()
        thread2.start()
        thread3.start()
        thread.join()
        thread2.join()
        thread3.join()
        print('Aggregated = true. Going to sleep.'+str(time.time()))
        time.sleep(300)
