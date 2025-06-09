import json 

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from django.contrib.auth.models import User
from .models import ChatRoom, Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        sender = User.objects.get(username="anon")

        room, _ = ChatRoom.objects.get_or_create(name=self.room_name)

        Message.objects.create(
            room=room,
            sender=sender,
            content=message
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                "type": "chat.message",
                "message": message,
                "sender": sender.username
            }
        )

    def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]

        self.send(text_data=json.dumps({
            "message": message,
            "sender": sender
        }))
    