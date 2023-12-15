from django.contrib.auth.models import User
import pytest
from apps.core.views import BaseView


@pytest.mark.django_db()
class TestBaseView:
    def test_get_user(self) -> None:
        user: User = User.objects.create_user(username="test", password="test")
        base_view: BaseView = BaseView()
        assert base_view.get_user(user.id) == user  # type: ignore
