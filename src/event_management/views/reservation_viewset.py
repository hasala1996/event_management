from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from event_management.models import Reservation
from event_management.serializers import (
    ReservationCreateUpdateSerializer,
    ReservationListSerializer,
)
from core.utils.verify_permission import verify_permission
from core.utils.authorizer_permission import AuthorizerPermission
from core.utils.pagination import CustomPageNumberPagination


class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reservations with CRUD operations.
    Includes custom business logic and permission verification.
    """

    queryset = Reservation.objects.all()
    serializer_class = ReservationListSerializer
    permission_classes = [AuthorizerPermission]
    pagination_class = CustomPageNumberPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["event", "status"]
    search_fields = ["event__name", "attendee__user__email"]
    ordering_fields = ["reservation_date"]
    ordering = ["reservation_date"]

    @verify_permission("view_reservation")
    def list(self, request, *args, **kwargs):
        """
        List reservations with filters and search capabilities.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ReservationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ReservationListSerializer(queryset, many=True)
        return Response(serializer.data)

    @verify_permission("view_reservation")
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve details of a specific reservation.
        """
        instance = self.get_object()
        serializer = ReservationListSerializer(instance)
        return Response(serializer.data)

    @verify_permission("add_reservation")
    def create(self, request, *args, **kwargs):
        """
        Create a reservation with custom validations.
        """
        serializer = ReservationCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @verify_permission("change_reservation")
    def update(self, request, *args, **kwargs):
        """
        Update a reservation with custom validations.
        """
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = ReservationCreateUpdateSerializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @verify_permission("delete_reservation")
    def destroy(self, request, *args, **kwargs):
        """
        Delete a reservation with custom validations.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
