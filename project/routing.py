"""Project asgi routing."""
# Django
from django.urls import re_path

# Project
from apps.door_opener.consumers import DoorStatusConsumer
from apps.watering_system.consumers import PumpStatusConsumer

websocket_urlpatterns = [
    re_path(r'ws/pump_status/$', PumpStatusConsumer.as_asgi()),
    re_path(r'ws/door_status/$', DoorStatusConsumer.as_asgi()),
]
