from django.conf.urls import url
from Exchanges import views
from django.conf.urls.static import static
from PiedPiper import settings
from .tick_exchparser import ThreadingT

# Здесь есть баг для некоторых пар, нужно фиксить.
urlpatterns = [

    url(r'^$', views.index_view, name='index'),

    url(r'^bittrex/$', views.Bittrex_view, name='Bittrex'),
    url(r'^bittrex/(?P<market>[A-Za-z]+-[A-Za-z]+)/$', views.Bittrex_view, name='bittrex/marketname'),
    url(r'^bittrex/(?P<market>[A-Za-z]+-\d[A-Za-z]+)/$', views.Bittrex_view, name='bittrex/2give'), #для названий с цифрой в начале
    url(r'^bittrex/(?P<market>[A-Za-z]+-[A-Za-z]+\d)/$', views.Bittrex_view, name='bittrex/emc2'),  #для названий с цифрой в конце

    url(r'^charts/$', views.ChartsView.as_view(), name='Charts'),
    url(r'^charts/(?P<market>[A-Za-z]+-[A-Za-z]+)/$', views.ChartsView.as_view(), name='charts/marketname'),
    url(r'^charts/(?P<market>[A-Za-z]+-\d[A-Za-z]+)/$', views.ChartsView.as_view(), name='charts/2give'),
    url(r'^charts/(?P<market>[A-Za-z]+-[A-Za-z]+\d)/$', views.ChartsView.as_view(), name='charts/emc2'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# STATIC_URL нужен для импорта css , img, js файлов из папки static

# URLS.PY загружается только один раз, как следствие запускать наш скрипт на обработку данных можно отсюда
# Необходимо для постоянного сбора данных. Вынесено в отдельный поток во избежания страданий основного из-за While(True)
# Make daemonic(!)
testingThreads = ThreadingT()
testingThreads.start()
