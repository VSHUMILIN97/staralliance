from django.conf.urls import url
from Exchanges import views
urlpatterns = [
    url(r'^bittrex/$', views.Bittrex_view, name='BittrexTick'),
    url(r'^charts/$', views.ChartsView.as_view(), name='Charts'),
]