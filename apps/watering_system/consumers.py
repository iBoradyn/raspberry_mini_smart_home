"""Watering system consumers."""
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class PumpStatusConsumer(WebsocketConsumer):
    group_name = 'pump_status'

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        pump_status = text_data_json["pump_status"]

        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "pump.status", "pump_status": pump_status}
        )

    def pump_status(self, event):
        pump_status = event["pump_status"]

        self.send(text_data=json.dumps({"pump_status": pump_status}))
