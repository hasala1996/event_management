from rest_framework import serializers
from event_management.models import Reservation


class ReservationListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing reservations.
    """

    event_name = serializers.CharField(source="event.name", read_only=True)
    attendee_email = serializers.CharField(source="attendee.user.email", read_only=True)

    class Meta:
        model = Reservation
        fields = ["id", "event_name", "attendee_email", "reservation_date", "status"]
