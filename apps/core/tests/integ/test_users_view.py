import json
from django.test.client import Client
from django.contrib.auth.models import User
from django.urls import reverse
import pytest


@pytest.mark.django_db()
class TestUsersView:
    def test_get_user_empty(self, client: Client) -> None:
        response = client.get(reverse("users"))
        assert response.status_code == 204

    def test_get_user(self, client: Client) -> None:
        User.objects.create_user(username="test", password="test")
        response = client.get("/api/users/")
        assert response.status_code == 200

    def test_create_user(self, client: Client) -> None:
        response = client.post(
            reverse("users"),
            json.dumps(
                dict(username="jordan95v", email="jordan@m.com", password="testtest"),
            ),
            content_type="application/json",
        )
        assert response.status_code == 201

    def test_create_user_already_exists(self, client: Client) -> None:
        User.objects.create_user(username="jordan95v", password="testtest")
        response = client.post(
            reverse("users"),
            json.dumps(
                dict(username="jordan95v", email="jordan@m.com", password="testtest"),
            ),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_create_user_bad_request(self, client: Client) -> None:
        response = client.post(
            reverse("users"),
            json.dumps(
                dict(username="jordan95v", email="jqqdqdq", password="test"),
            ),
            content_type="application/json",
        )
        assert response.status_code == 400
