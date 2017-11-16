from django.conf.urls import url
from . import views
from django.db import models

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
]

