from django.conf.urls import url
from exchanger.consumers import ArbitrationConsumer

channel_routing = [
    url(r"", ArbitrationConsumer),
]
