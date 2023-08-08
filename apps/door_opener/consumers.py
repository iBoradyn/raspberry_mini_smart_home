"""Door opener consumers."""
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class DoorStatusConsumer(WebsocketConsumer):
    group_name = 'door_status'

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
        door_status = text_data_json["door_status"]

        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "door.status", "door_status": door_status}
        )

    def door_status(self, event):
        door_status = event["door_status"]

        self.send(text_data=json.dumps({"door_status": door_status}))
