from django.conf.urls import url
from Exchanges import views
urlpatterns = [
    url(r'^bittrex/$', views.Bittrex_view, name='Bittrex'),
    url(r'^bittrex/(?P<market>[A-Za-z]+-[A-Za-z]+)/$', views.Bittrex_view, name='bittrex/marketname'),
    url(r'^bittrex/(?P<market>[A-Za-z]+-\d[A-Za-z]+)/$', views.Bittrex_view, name='bittrex/2give'), #для названий с цифрой в начале
    url(r'^bittrex/(?P<market>[A-Za-z]+-[A-Za-z]+\d)/$', views.Bittrex_view, name='bittrex/emc2'),  #для названий с цифрой в конце

    url(r'^charts/$', views.ChartsView.as_view(), name='Charts'),
    url(r'^charts/(?P<market>[A-Za-z]+-[A-Za-z]+)/$', views.ChartsView.as_view(), name='charts/marketname'),
    url(r'^charts/(?P<market>[A-Za-z]+-\d[A-Za-z]+)/$', views.ChartsView.as_view(), name='charts/2give'),
    url(r'^charts/(?P<market>[A-Za-z]+-[A-Za-z]+\d)/$', views.ChartsView.as_view(), name='charts/emc2'),
]