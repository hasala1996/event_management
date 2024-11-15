from django.db import models

from core.management.commands.base_model import (
    BaseModel,
)
from security.models import User


class Attendee(BaseModel):
    """
    Represents an attendee who can register for an event.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.email

    class Meta:
        db_table = "attendee"
