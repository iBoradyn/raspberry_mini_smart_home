"""Door opener consumers."""
# Standard Library
import json

# 3rd-party
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class DoorStatusConsumer(WebsocketConsumer):  # noqa: D101
    group_name = 'door_status'

    def connect(self):  # noqa: D102
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):  # noqa: D102
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):  # noqa: D102
        text_data_json = json.loads(text_data)
        door_status = text_data_json['door_status']

        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {'type': 'door.status', 'door_status': door_status}
        )

    def door_status(self, event):  # noqa: D102
        door_status = event['door_status']

        self.send(text_data=json.dumps({'door_status': door_status}))
