from django.core.management.base import BaseCommand, CommandError
from mongo_db_connection import MongoDBConnection
import logging
import atexit
import time
from process_manager import children_kill, proc_start

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Вызов экземпляра класс MongoDBConnection из файла mongo_db_connection
        #connectme = MongoDBConnection()
        # Подключение к БД PiedPiperStock(Дебаговая БД) После подключения все концы сбрасывает, так что технически безопасно
        #db = connectme.start_db().PiedPiperStock

        #
        # URLS.PY загружается только один раз, как следствие запускать наш скрипт на обработку данных можно отсюда
        # Необходимо для постоянного сбора данных. Вынесено в отдельный поток во избежания страданий основного из-за While(True)
        # Make daemonic(!) ПРОДУМАТЬ БЕЗОПАСНОСТЬ!
        logging.info(u'Server started')
        # testing_threads = ThreadingT()

        try:
            # testing_threads.start()
            logging.info(u'Threads"re successfully started')
            proc_start()
            while ( True ):
                time.sleep(0.1)

        except():
            logging.critical(u'Threads were not started')

        atexit.register(children_kill)
