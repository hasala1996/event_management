from rest_framework import serializers
from event_management.models import Reservation, Event
from core.utils.errors import CustomAPIException, FormErrors
from django.utils import timezone


class ReservationCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating reservations.
    """

    class Meta:
        model = Reservation
        fields = ["event", "attendee", "reservation_date", "status"]

    def validate_event(self, value):
        """
        Validate that the event exists and has available slots.
        """
        if value.date < timezone.now():
            raise CustomAPIException(
                detail=FormErrors.INVALID_DATE["message"],
                code=FormErrors.INVALID_DATE["code"],
            )
        if self.instance is None:  # Solo al crear una reserva
            # Verifica si hay slots disponibles
            confirmed_reservations = value.reservation_set.filter(
                status="Confirmed"
            ).count()
            if confirmed_reservations >= value.total_slots:
                raise CustomAPIException(
                    detail="This event has no available slots.",
                    code="no_available_slots",
                )

        return value

    def validate(self, attrs):
        """
        Ensure the user has not already reserved for the same event.
        """
        attendee = attrs.get("attendee")
        event = attrs.get("event")
        if Reservation.objects.filter(attendee=attendee, event=event).exists():
            raise CustomAPIException(
                detail=FormErrors.DUPLICATE_RESERVATION["message"],
                code=FormErrors.DUPLICATE_RESERVATION["code"],
            )
        return attrs
