import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from channels.testing import WebsocketCommunicator
from chat_project.asgi import application

user_model = get_user_model()
index_url = reverse('index')


@pytest.mark.django_db
def test_index_view(client):
    response = client.get(index_url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_index_view_logged(client):
    user = user_model.objects.create(username="test", password="test")
    client.force_login(user=user)
    response = client.get(index_url)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_chat_consumer():
    communicator = WebsocketCommunicator(application, "/ws/chat/test/")
    communicator.scope['headers'] = [
        (b'origin', b'http://localhost')
    ]
    connected, _ = await communicator.connect()
    assert connected