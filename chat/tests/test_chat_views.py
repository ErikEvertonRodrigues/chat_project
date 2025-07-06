import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

user_model = get_user_model()
url = reverse('index')


@pytest.mark.django_db
def test_index_view(client):
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_index_view_logged(client):
    user = user_model.objects.create(username="test", password="test")
    client.force_login(user=user)
    response = client.get(url)
    assert response.status_code == 200

