from django.db import models

from core.management.commands.base_model import (
    BaseModel,
)


class Speaker(BaseModel):
    """
    Represents a speaker or lecturer at an event.
    """

    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "speaker"
