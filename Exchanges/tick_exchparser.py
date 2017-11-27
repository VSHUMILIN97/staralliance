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

    def random_seed(self):
        while 1:
            try:
                timeTemp = random.uniform(10, 12.5)  # Значения можно менять
                print(timeTemp)
                # По вполне очевидным причинам забито в комментарий
                # api_get_getmarketsummaries()
                # api_get_getmarkethistory()
                # api_get_getticker()
                time.sleep(timeTemp)
            except:
                print('Overflow error in tick_exchparser')

    def aggregation_trigger(self):
        # DO SOMETHING GOOD UNLESS I'LL DELETE YOU (c) AngryDev
        None