from django.conf.urls import url, include
from exchanger import views
from django.conf.urls.static import static
from PiedPiper import settings

urlpatterns = [url(r'^exchange/$', views.Exchanger.as_view(), name='Exchange'),
               url(r'^exchange/(?P<room_name>[^/]+)/$', views.room, name='room'),

               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
