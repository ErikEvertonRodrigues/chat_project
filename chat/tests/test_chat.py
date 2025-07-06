from ..models import ChatRoom
import pytest

# Create your tests here.

@pytest.mark.django_db
def test_create_room():
    room_name = "room-name-test"
    room = ChatRoom.objects.create(name=room_name)
    assert ChatRoom.objects.count() == 1
    assert room.name == room_name

