import os
import subprocess
import sys
import signal
import atexit
from django.conf.urls import url
from Exchanges import views
from django.conf.urls.static import static
from PiedPiper import settings
from .tick_exchparser import ThreadingT, aggregation_trigger
from threading import Thread
from mongo_db_connection import MongoDBConnection
import logging


# Здесь есть баг для некоторых пар, нужно фиксить.
urlpatterns = [

    url(r'^$', views.index_view, name='index'),

    url(r'^bittrex/$', views.Bittrex_view, name='Bittrex'),
    url(r'^bittrex/(?P<pair>[A-Za-z]+-[A-Za-z]+)/$', views.Bittrex_view, name='bittrex/marketname'),
    url(r'^bittrex/(?P<pair>[A-Za-z]+-\d[A-Za-z]+)/$', views.Bittrex_view, name='bittrex/2give'),
    # для названий с цифрой в начале
    url(r'^bittrex/(?P<pair>[A-Za-z]+-[A-Za-z]+\d)/$', views.Bittrex_view, name='bittrex/emc2'),
    # для названий с цифрой в конце

    url(r'^charts/$', views.ChartsView.as_view(), name='Charts'),
    url(r'^charts/(?P<exchange>.+)/(?P<pair>.+)/$', views.ChartsView.as_view(), name='charts/marketname'),

    url(r'^compare/$', views.Comparison.as_view(), name='Comparison'),
    url(r'^compare/(?P<mode>.+)/$', views.Comparison.as_view(), name='Comparison'),  # выставить compare для другой страницы
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# STATIC_URL нужен для импорта css , img, js файлов из папки static

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


# Вызов экземпляра класс MongoDBConnection из файла mongo_db_connection
connectme = MongoDBConnection()
# Подключение к БД PiedPiperStock(Дебаговая БД) После подключения все концы сбрасывает, так что технически безопасно
db = connectme.start_db().PiedPiperStock
#
# URLS.PY загружается только один раз, как следствие запускать наш скрипт на обработку данных можно отсюда
# Необходимо для постоянного сбора данных. Вынесено в отдельный поток во избежания страданий основного из-за While(True)
# Make daemonic(!) ПРОДУМАТЬ БЕЗОПАСНОСТЬ!
logging.info(u'Server started')
testingThreads = ThreadingT()
t2 = Thread(target=aggregation_trigger)

# В качестве подпроцесса child выбираем скрипт websocketapp.py
# В качестве аргументов для начала работы подпроцесса передаем команду execute и указываем на потомка
# Далее открываем субпроцесс, в качестве "входа" используем PIPE.
child = os.path.join(os.path.dirname(__file__), "../websocketapp.py")
command = [sys.executable, child]
pipe = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

child_pid = pipe.pid


def child_kill():
    if child_pid is None:
        pass
    else:
        os.kill(child_pid, signal.SIGTERM)
        logging.info(u'WebSocket rundown')


try:
    testingThreads.start()
    t2.start()
    logging.info(u'Threads"re successfully started')
except():
    logging.critical(u'Threads were not started')

atexit.register(child_kill)
