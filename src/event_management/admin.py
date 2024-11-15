from django.contrib import admin
from .models import Event, Reservation
from .forms import EventForm
from .actions import (
    make_events_featured,
    mark_reservations_confirmed,
    mark_reservations_no_confirmed,
)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Event model instances.

    Utilizes a custom form for event data entry. Displays a list of events with
    their name, date, location, category, and featured status. Allows filtering
    by date, category, and location, and searching by name, description, location,
    and category. Events are ordered by date. Includes an action to mark events as featured.
    """

    form = EventForm
    list_display = ("name", "date", "location", "category", "is_featured")
    list_filter = ("date", "category", "location")
    search_fields = ("name", "description", "location", "category")
    ordering = ["date"]
    actions = [make_events_featured]
    fieldsets = (
        (None, {"fields": ("name", "description", "date", "is_featured")}),
        (
            "Location and Category Details",
            {"fields": ("location", "category")},
        ),
        (
            "Speakers",
            {
                "fields": ("speakers",),
            },
        ),
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Reservation model instances.

    Displays a list of reservations showing the event, attendee, reservation date,
    and status. Supports filtering by status and reservation date, and searching
    by event name and attendee's email. Reservations are ordered by reservation date.
    Includes an action to mark reservations as confirmed.
    """

    list_display = ("event", "attendee", "reservation_date", "status")
    list_filter = ("status", "reservation_date")
    search_fields = ("event__name", "attendee__user__email")
    ordering = ["reservation_date"]
    actions = [mark_reservations_confirmed, mark_reservations_no_confirmed]
