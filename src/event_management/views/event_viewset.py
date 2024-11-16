from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from event_management.models import Event, Attendee
from event_management.serializers import EventSerializer, EventCreateUpdateSerializer
from core.utils.authorizer_permission import AuthorizerPermission
from .filters import EventFilter
from core.utils.verify_permission import verify_permission
from rest_framework.decorators import action
from core.utils.pagination import CustomPageNumberPagination


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing events with CRUD operations, search, filtering, pagination, and ordering.
    Includes custom business logic in overridden methods.
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AuthorizerPermission]
    pagination_class = CustomPageNumberPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = EventFilter
    search_fields = ["name", "description"]
    ordering_fields = ["date", "name"]
    ordering = ["date"]

    @verify_permission("view_event")
    def list(self, request, *args, **kwargs):
        """
        Overrides list method to handle custom logic before listing Events.

        Returns:
            Response: A paginated list of all events.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @verify_permission("view_event")
    def retrieve(self, request, *args, **kwargs):
        """
        Overrides retrieve method to handle custom logic before retrieving a single Event.

        Returns:
            Response: The serialized data of a single event.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @verify_permission("add_event")
    def create(self, request, *args, **kwargs):
        """
        Overrides create method to handle custom logic before creating an Event.
        """
        serializer = EventCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @verify_permission("change_event")
    def update(self, request, *args, **kwargs):
        """
        Overrides update method to handle custom logic before updating an Event.
        """
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = EventCreateUpdateSerializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @verify_permission("delete_event")
    def destroy(self, request, *args, **kwargs):
        """
        Overrides destroy method to handle custom logic before deleting an Event.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=["get"], url_path="list-events", url_name="list_events"
    )
    def list_events(self, request):
        """
        Custom action to list events with their name and ID.
        """
        events = Event.objects.values("id", "name")
        return Response(events, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path="list-attendees",
        url_name="list_attendees",
    )
    def list_attendees(self, request):
        """
        Custom action to list attendees with their full name and ID.
        """
        attendees = Attendee.objects.values("id", "user__first_name", "user__last_name")
        formatted_attendees = [
            {
                "id": attendee["id"],
                "full_name": f"{attendee['user__first_name']} {attendee['user__last_name']}",
            }
            for attendee in attendees
        ]
        return Response(formatted_attendees, status=status.HTTP_200_OK)
