from rest_framework import serializers
from event_management.models import Event, Category
from django.utils import timezone
from core.utils.errors import FormErrors, CustomAPIException


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Event instances.
    """

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "description",
            "date",
            "location",
            "is_featured",
            "category",
        ]

    def validate_date(self, value):
        """
        Validates that the event date is in the future.

        Parameters:
            value (datetime): The date of the event.

        Raises:
            CustomAPIException: If the date is in the past.

        Returns:
            datetime: The validated event date.
        """
        if value < timezone.now():
            raise CustomAPIException(
                detail=FormErrors.INVALID_DATE["message"],
                code=FormErrors.INVALID_DATE["code"],
            )
        return value

    def validate(self, attrs):
        """
        Custom validation for the entire Event data.

        Checks if the event is marked as featured and has a description.

        Parameters:
            attrs (dict): The validated data for the Event.

        Raises:
            CustomAPIException: If an event is marked as featured without a description.

        Returns:
            dict: The validated attributes for the Event.
        """
        if attrs.get("is_featured") and not attrs.get("description"):
            raise CustomAPIException(
                detail=FormErrors.MISSING_DESCRIPTION["message"],
                code=FormErrors.MISSING_DESCRIPTION["code"],
            )
        return attrs

    def update(self, instance, validated_data):
        """
        Handles partial updates for Event instances.
        """
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
