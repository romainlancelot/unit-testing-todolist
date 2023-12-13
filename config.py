import re
from typing import ClassVar

__all__: list[str] = ["config"]


class Config:
    NAME_REGEX: ClassVar[re.Pattern] = re.compile(r"^[a-zA-Z\- ]{2,40}$")
    MAX_TODOLIST_CAPACITY: ClassVar[int] = 10
    SEND_MAIL_THRESHOLD: ClassVar[int] = 8
    REQUIRED_AGE: ClassVar[int] = 13
    MINUTES_THRESHOLD: ClassVar[int] = 30


config: Config = Config()
