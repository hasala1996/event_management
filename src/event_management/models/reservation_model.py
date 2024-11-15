from django.db import models

from core.management.commands.base_model import (
    BaseModel,
)
from event_management.models import Event, Attendee


class Reservation(BaseModel):
    """
    Represents a reservation that an attendee makes for an event.
    """

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="reservations"
    )
    attendee = models.ForeignKey(
        Attendee, on_delete=models.CASCADE, related_name="reservations"
    )
    reservation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")

    class Meta:
        db_table = "reservation"
        ordering = ["reservation_date"]
        unique_together = ("event", "attendee")

    def __str__(self):
        return f"{self.attendee.user.email} - {self.event.name}"
