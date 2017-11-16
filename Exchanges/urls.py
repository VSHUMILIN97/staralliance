from django.conf.urls import url
from Exchanges import views
urlpatterns = [
    url(r'^Bittrex/$', views.Bittrex_view, name='Bittrex'),
]