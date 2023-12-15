import json
from django.test.client import Client
from django.contrib.auth.models import User
from django.urls import reverse
import pytest
from apps.core.models import Item


@pytest.mark.django_db()
class TestItemsView:
    def test_get_items_no_user(self, client: Client) -> None:
        response = client.get(reverse("todolist", kwargs=dict(user_id=1)))
        assert response.status_code == 400

    def test_get_user_items_empty(self, client: Client) -> None:
        User.objects.create_user(username="test", password="test")
        response = client.get(reverse("todolist", kwargs=dict(user_id=1)))
        assert response.status_code == 200
        assert response.json() == dict(status="success", items=[])

    def test_get_user_items(self, client: Client) -> None:
        user: User = User.objects.create_user(username="test", password="test")
        for i in range(10):
            Item.objects.create(name=f"item{i}", content=f"content{i}", user=user)
        response = client.get(reverse("todolist", kwargs=dict(user_id=1)))
        assert response.status_code == 200
        assert len(response.json()["items"]) == 10

    def test_create_item(self, client: Client) -> None:
        user: User = User.objects.create_user(username="test", password="test")
        response = client.post(
            reverse("todolist", kwargs=dict(user_id=user.id)),  # type: ignore
            json.dumps(dict(name="item", content="content")),
            content_type="application/json",
        )
        assert response.status_code == 201

    def test_create_item_no_user(self, client: Client) -> None:
        response = client.post(
            reverse("todolist", kwargs=dict(user_id=1)),
            json.dumps(dict(name="item", content="content")),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_create_item_bad_request(self, client: Client) -> None:
        user: User = User.objects.create_user(username="test", password="test")
        response = client.post(
            reverse("todolist", kwargs=dict(user_id=user.id)),  # type: ignore
            json.dumps(dict(name="item", content="", dunno="test")),
            content_type="application/json",
        )
        assert response.status_code == 400
