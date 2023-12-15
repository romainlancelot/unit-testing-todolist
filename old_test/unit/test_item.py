from datetime import datetime, UTC
from pathlib import Path
import pytest
from core.exceptions import ItemNotValid
from core.models import Item


class TestItem:
    @pytest.mark.parametrize(
        "data, throwable",
        [
            (dict(name="Do laundry", content="My wife is angry, please help"), None),
            (dict(name="Do laundry", content=""), None),
            (
                dict(
                    name="Do laundry",
                    content=Path("tests/samples/todo_list_sample.txt").read_text(
                        encoding="utf-8"
                    ),
                ),
                ItemNotValid,
            ),
            (dict(name="", content="My wife is angry, please help"), ItemNotValid),
        ],
    )
    def test_is_valid(
        self, data: dict[str, str], throwable: type[Exception] | None
    ) -> None:
        item: Item = Item(**data)
        if throwable is not None:
            with pytest.raises(throwable):
                item.is_valid()
        else:
            item.is_valid()

    def test_init(self) -> None:
        item: Item = Item(name="Do laundry", content="My wife is angry, please help")
        target_date: str = datetime.now(UTC).strftime("%Y-%m-%d")
        assert item.creation_date.strftime("%Y-%m-%d") == target_date
