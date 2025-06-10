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

        room, _ = ChatRoom.objects.get_or_create(name=self.room_name)
        messages = Message.objects.filter(room=room).order_by("-timestamp")[:50]


        for message in messages:
            print(message.sender.username)
            self.send(text_data=json.dumps({
                "type": "chat.history",
                "message": message.content,
                "sender": message.sender.username if message.sender else "anonymous",
                "timestamp": message.timestamp.isoformat()
            }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]

            sender, _ = User.objects.get_or_create(username="anon")

            room, _ = ChatRoom.objects.get_or_create(name=self.room_name)

            message_obj = Message.objects.create(
                room=room,
                sender=sender,
                content=message
            )

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, 
                {
                    "type": "chat.message",
                    "message": message_obj.content,
                    "sender": message_obj.sender.username,
                    "timestamp": message_obj.timestamp.isoformat()
                }
            )
        except Exception as e:
            print("THERE IS A ERROR RIGHT HERE IN RECEIVE: ", e)

    def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        timestamp = event["timestamp"]

        self.send(text_data=json.dumps({
            "type": "chat.message",
            "message": message,
            "sender": sender if sender else "anonymous",
            "timestamp": timestamp
        }))
    