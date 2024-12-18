from django.db import models

from core.management.commands.base_model import BaseModel
from event_management.models import Category, Speaker


class Event(BaseModel):
    """
    Represents an event, which may be a conference or workshop.
    """

    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="events"
    )
    speakers = models.ManyToManyField(Speaker, related_name="events")
    is_featured = models.BooleanField(default=False)
    total_slots = models.PositiveIntegerField(default=0)

    @property
    def available_slots(self):
        """
        Calculate the number of available slots for the event.

        Returns:
            int: The number of available slots.
        """
        confirmed_reservations = self.reservation_set.filter(status="Confirmed").count()
        return max(self.total_slots - confirmed_reservations, 0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "event"
        ordering = ["date"]
        permissions = [
            ("create_event", "Can create event"),
            ("edit_event", "Can edit event"),
        ]
