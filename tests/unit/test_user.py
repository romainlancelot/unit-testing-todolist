from datetime import UTC, datetime, timedelta
from typing import Any
from unittest.mock import MagicMock
import pytest
from pytest_mock import MockerFixture
from core.exceptions import ItemNotValid, TodolistMaximumCapacity, UserNotValid
from core.models import EmailSenderService, Item, User
from config import config

CORRECT_AGE: datetime = datetime.now() - timedelta(days=365 * config.REQUIRED_AGE)
BAD_AGE: datetime = datetime.now() - timedelta(days=365 * (config.REQUIRED_AGE - 1))


@pytest.fixture
def user() -> User:
    return User(
        first_name="Jordan",
        last_name="Dufresne",
        email="jordan@dufresne.com",
        password="Password123",
        birth_date=datetime.now() - timedelta(days=365 * config.REQUIRED_AGE),
    )


class TestUser:
    @pytest.mark.parametrize(
        "data, throwable",
        [
            (
                dict(
                    first_name="Jordan",
                    last_name="Dufresne",
                    email="jordan@dufresne.fr",
                    password="Password123",
                    birth_date=CORRECT_AGE,
                ),
                None,
            ),
            (
                dict(
                    first_name="",
                    last_name="Lancelot",
                    email="romain@lancelot.fr",
                    password="Password123",
                    birth_date=CORRECT_AGE,
                ),
                UserNotValid,
            ),
            (
                dict(
                    first_name="Jordan",
                    last_name="",
                    email="jordan@dufresne.fr",
                    password="Password123",
                    birth_date=CORRECT_AGE,
                ),
                UserNotValid,
            ),
            (
                dict(
                    first_name="Romain",
                    last_name="",
                    email="romain@@@lancelot//.....fr",
                    password="Password123",
                    birth_date=CORRECT_AGE,
                ),
                UserNotValid,
            ),
            (
                dict(
                    first_name="Romain",
                    last_name="Lancelot",
                    email="romain@lancelot.fr",
                    password="password_not_valid",
                    birth_date=CORRECT_AGE,
                ),
                UserNotValid,
            ),
            (
                dict(
                    first_name="Romain",
                    last_name="Lancelot",
                    email="romain@lancelot.fr",
                    password="Password123",
                    birth_date=BAD_AGE,
                ),
                UserNotValid,
            ),
        ],
    )
    def test_is_valid(
        self, data: dict[str, Any], throwable: type[Exception] | None
    ) -> None:
        user: User = User(**data)
        if throwable is not None:
            with pytest.raises(throwable):
                user.is_valid()
        else:
            user.is_valid()

    @pytest.mark.parametrize(
        "todolist, item, creation_date, throwable, expected_len",
        [
            (
                [Item(name="Do laundry", content="My wife is angry, please help")],
                Item(name="Clean room", content="Mom angry."),
                datetime.now(UTC) + timedelta(minutes=config.MINUTES_THRESHOLD),
                None,
                2,
            ),
            (
                [Item(name="Do laundry", content="My wife is angry, please help")],
                Item(name="Do laundry", content="Mom angry."),
                datetime.now(UTC) + timedelta(minutes=config.MINUTES_THRESHOLD),
                ItemNotValid,
                1,
            ),
            (
                [Item(name="Do laundry", content="My wife is angry, please help")],
                Item(name="Clean room", content="Mom angry."),
                datetime.now(UTC) + timedelta(minutes=config.MINUTES_THRESHOLD - 10),
                ItemNotValid,
                1,
            ),
            (
                [Item(name="Do laundry", content="My wife is angry, please help")] * 10,
                Item(name="Clean room", content="Mom angry."),
                datetime.now(UTC) + timedelta(minutes=config.MINUTES_THRESHOLD),
                TodolistMaximumCapacity,
                1,
            ),
            (
                [Item(name="Do laundry", content="My wife is angry, please help")] * 7,
                Item(name="Clean room", content="Mom angry."),
                datetime.now(UTC) + timedelta(minutes=config.MINUTES_THRESHOLD),
                None,
                8,
            ),
        ],
    )
    def test_add_item(
        self,
        user: User,
        todolist: list[Item],
        item: Item,
        creation_date: datetime,
        throwable: type[Exception] | None,
        expected_len: int,
        mocker: MockerFixture,
    ) -> None:
        mocker.patch.object(User, "is_valid")
        mocker.patch.object(Item, "is_valid")
        mocker.patch.object(User, "save_todolist_in_db")
        email_mock: MagicMock = mocker.patch.object(EmailSenderService, "send_email")
        user.todo_list = todolist
        item.creation_date = creation_date
        if throwable is not None:
            with pytest.raises(throwable):
                user.add_item(item)
                assert len(user.todo_list) == expected_len
        else:
            user.add_item(item)
            assert len(user.todo_list) == expected_len
            if expected_len == config.MINUTES_THRESHOLD:
                email_mock.assert_called_once_with(user, "Todo list almost full")

    def test_add_item_bad_user(self, user: User, mocker: MockerFixture) -> None:
        item: Item = Item(name="Do laundry", content="My wife is angry, please help")
        mocker.patch.object(User, "is_valid", side_effect=UserNotValid)
        with pytest.raises(UserNotValid):
            user.add_item(item)

    def test_add_item_bad_item(self, user: User, mocker: MockerFixture) -> None:
        item: Item = Item(name="Do laundry", content="My wife is angry, please help")
        mocker.patch.object(Item, "is_valid", side_effect=ItemNotValid)
        with pytest.raises(ItemNotValid):
            user.add_item(item)

    def test_save_todolist_in_db(self, user: User) -> None:
        with pytest.raises(NotImplementedError):
            user.save_todolist_in_db()
