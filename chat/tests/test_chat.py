from django.contrib.auth import get_user_model
from ..models import ChatRoom, Message
import pytest

# Create your tests here.
user_model = get_user_model()
room_name = "room-name-test"
@pytest.mark.django_db
def test_create_room():
    room = ChatRoom.objects.create(name=room_name)
    assert ChatRoom.objects.count() == 1
    assert room.name == room_name

@pytest.mark.django_db
def test_create_message():
    room = ChatRoom.objects.create(name=room_name)
    user = user_model.objects.create(username="test", password="test")
    content = "This is a test message"
    message = Message.objects.create(room=room, sender=user, content=content)
    assert Message.objects.count() == 1
    assert message.room.name == room_name
    assert message.sender == user
    assert message.content == content

