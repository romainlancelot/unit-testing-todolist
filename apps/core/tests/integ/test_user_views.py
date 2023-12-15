from django.http import HttpResponse
from django.test.client import Client
import pytest


@pytest.mark.django_db()
class TestUserView:
    def test_get_user(self, client: Client) -> None:
        response = client.get("/api/users/")
        assert response.status_code == 204
