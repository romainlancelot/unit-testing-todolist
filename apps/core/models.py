from typing import Any
from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    content: models.TextField = models.TextField()
    creation_date: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    user: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="items"
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert the item to a dictionary.

        Returns:
            dict[str, str]: The item as a dictionary.
        """

        return dict(
            id=self.id,  # type: ignore
            name=self.name,
            content=self.content,
            creation_date=self.creation_date.isoformat(),
        )
