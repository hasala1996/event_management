from django_filters import rest_framework as filters
from event_management.models import Event


class EventFilter(filters.FilterSet):
    """
    Custom filter for Event to allow filtering by category name
    using 'category' as the URL parameter.
    """

    category = filters.CharFilter(field_name="category__name", lookup_expr="iexact")
    date = filters.DateFilter(field_name="date")

    class Meta:
        model = Event
        fields = []
