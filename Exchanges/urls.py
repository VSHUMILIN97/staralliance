from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from Exchanges import views
from django.conf.urls.static import static
from PiedPiper import settings


urlpatterns = [

    url(r'^bittrex/$', views.Bittrex_view, name='Bittrex'),
    url(r'^bittrex/(?P<pair>[A-Za-z]+-[A-Za-z]+)/$', views.Bittrex_view, name='bittrex/marketname'),
    url(r'^bittrex/(?P<pair>[A-Za-z]+-\d[A-Za-z]+)/$', views.Bittrex_view, name='bittrex/2give'),

    # для названий с цифрой в начале
    url(r'^bittrex/(?P<pair>[A-Za-z]+-[A-Za-z]+\d)/$', views.Bittrex_view, name='bittrex/emc2'),
    # для названий с цифрой в конце

    url(r'^charts/$', views.ChartsView.as_view(), name='Charts'),
    url(r'^charts/(?P<exchange>.+)/(?P<pair>.+)/$', views.ChartsView.as_view(), name='charts/marketname'),

    url(r'^compare/$', views.Comparison.as_view(), name='Comparison'),  # ADD login_required
    url(r'^compare/(?P<mode>.+)/$', views.Comparison.as_view(), name='Comparison'),  # ADD login_required
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# STATIC_URL upload all our /static/ files. Full definition in root/static/INFO.txt
