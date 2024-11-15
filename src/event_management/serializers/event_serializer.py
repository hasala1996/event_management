from rest_framework import serializers
from event_management.models import Event
from datetime import datetime
from core.utils.errors import FormErrors, CustomAPIException
from django.utils import timezone


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model with custom validation and business logic.
    """

    category = serializers.SerializerMethodField()

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

    def get_category(self, obj):
        """
        Custom method to return category details with both id and name.

        Parameters:
            obj (Event): The event instance being serialized.

        Returns:
            dict: A dictionary containing the id and name of the category.
        """
        category = obj.category
        return {"id": category.id, "name": category.name} if category else None
