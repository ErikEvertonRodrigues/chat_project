from django.test import TestCase
from .models import ChatRoom

# Create your tests here.

class ChatRoomModelTest(TestCase):
    def test_create_room(self):
        room_name = "testroom"
        room = ChatRoom.objects.create(name=room_name)
        self.assertEqual(room.name, room_name)
        self.assertIsNotNone(room.created_at)
