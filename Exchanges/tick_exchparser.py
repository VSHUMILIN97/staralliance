from Exchanges.BittrexObjCreate import api_get_getmarkethistory, api_get_getticker, api_get_getmarketsummaries
import random
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
        # писон позволяет/ Безопасность из говна и палок, как и код. Доработать со временем!
        while 1:
            try:
                timeTemp = random.uniform(10, 12.5)  # Значения можно менять
                print(timeTemp)
                try:
                    print('1')
                    # t1 = Thread(target=api_get_getmarketsummaries)
                    # t2 = Thread(target=api_get_getmarkethistory)
                    # t3 = Thread(target=api_get_getticker)
                    # t1._stop()
                    # t2._stop()
                    # t3._stop()
                    # t1.start()
                    # t2.start()
                    # t3.start()
                    # t1.join()
                    # t2.join()
                    # t3.join()
                except(Exception):
                    print('Mistake in random_seed')
                time.sleep(timeTemp)
            except:
                print('Overflow error in tick_exchparser')

def aggregation_trigger():
    while 1:
         print('Alive')
         # Примерный макет
         # TimeAggregator.flag = True
         # TimeAggregator.startcompile()
         print('Queries are ready')
         time.sleep(8)
