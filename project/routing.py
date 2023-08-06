"""Project asgi routing."""
from django.urls import re_path

from apps.watering_system.consumers import PumpStatusConsumer
from apps.door_opener.consumers import MotorStatusConsumer

websocket_urlpatterns = [
    re_path(r'ws/pump_status/$', PumpStatusConsumer.as_asgi()),
    re_path(r'ws/motor_status/$', MotorStatusConsumer.as_asgi()),
]