"""Door opener consumers."""
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class MotorStatusConsumer(WebsocketConsumer):
    group_name = 'motor_status'

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
        motor_status = text_data_json["motor_status"]

        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "motor.status", "motor_status": motor_status}
        )

    def motor_status(self, event):
        motor_status = event["motor_status"]

        self.send(text_data=json.dumps({"motor_status": motor_status}))
