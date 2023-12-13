from dataclasses import dataclass, field
from datetime import datetime, UTC, timedelta
import re
from core.exceptions import ItemNotValid, TodolistMaximumCapacity, UserNotValid
from config import config

__all__: list[str] = ["Item", "User", "EmailSenderService"]


class Item:
    def __init__(self, name: str, content: str) -> None:
        self.name: str = name
        self.content: str = content
        self.creation_date: datetime = datetime.now(UTC)

    def is_valid(self) -> None:
        """Check if the item is valid.

        Raises:
            ItemNotValid: If the content is too long or the name is not valid.
        """

        if len(self.content) > 1000:
            raise ItemNotValid("Content is too long")
        if not config.NAME_REGEX.match(self.name):
            raise ItemNotValid("Name is not valid")


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    password: str
    birth_date: datetime
    todo_list: list[Item] = field(default_factory=list)

    def is_valid(self) -> None:
        """Validates the user object by checking all attributes.

        Raises:
            UserNotValid: If any of the fields are not valid, with error message.
        """

        # Check email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise UserNotValid("Email is not valid")

        # Check password
        password_regex: str = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,40}$"
        if not re.match(password_regex, self.password):
            raise UserNotValid("Password is not valid")

        # Check first and last name
        if not config.NAME_REGEX.match(self.first_name):
            raise UserNotValid("First name is not valid")
        if not config.NAME_REGEX.match(self.last_name):
            raise UserNotValid("Last name is not valid")

        # Check birth date
        if self.birth_date.year + 13 > datetime.now(UTC).year:
            raise UserNotValid("Birth date is not valid")

    def add_item(self, item: Item) -> None:
        """Adds an item to the user's todo list.

        Args:
            item: The item to add to the todo list.

        Raises:
            TodolistMaximumCapacity: If the todo list is already at maximum capacity.
            ItemNotValid: If the item already exists in the todo list or its creation
                date is too close to another item.
        """

        self.is_valid()
        item.is_valid()

        if len(self.todo_list) == config.MAX_TODOLIST_CAPACITY:
            raise TodolistMaximumCapacity("Todo list is full")

        for element in self.todo_list:
            if element.name == item.name:
                raise ItemNotValid("Item already exists in user todo list")
            target_date: datetime = item.creation_date - timedelta(
                minutes=config.MINUTES_THRESHOLD
            )
            if target_date < element.creation_date:
                err_message: str = "Item creation date is too close to another item"
                raise ItemNotValid(err_message)

        print(f'Item "{item.name}"added to user todo list')
        self.todo_list.append(item)

        if len(self.todo_list) == config.SEND_MAIL_THRESHOLD:
            EmailSenderService.send_email(self, "Todo list almost full")

        self.save_todolist_in_db()

    def save_todolist_in_db(self) -> None:
        raise NotImplementedError("Not implemented yet")  # pragma: no cover


class EmailSenderService:
    @classmethod
    def send_email(cls, user: User, content: str) -> None:
        raise NotImplementedError("Not implemented yet")  # pragma: no cover
