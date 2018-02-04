from pymongo import MongoClient
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


# Класс с функцией для соединения с БД. В дальнейшем количество методов вырастет.
# По крайней мере мы на это расчитываем.
class MongoDBConnection:
    # Организует коннект к базе данных. Возвращает объект MongoClient для дальнейшей работы с БД.
    def start_db(self):
        connect = MongoClient('localhost', 27017)
        logging.info(u'Connection to the MONGODB has been established')
        return connect

    def stop_connect(self):
        self.start_db().close()