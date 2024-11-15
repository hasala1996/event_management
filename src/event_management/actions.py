from django.contrib import admin


def update_field(queryset, field_name, value):
    """
    Generic function to update a specific field in the given queryset.

    Parameters:
        queryset (QuerySet): A QuerySet containing the selected objects.
        field_name (str): The name of the field to update.
        value: The value to set for the field.
    """
    queryset.update(**{field_name: value})


@admin.action(description="Mark selected events as featured")
def make_events_featured(modeladmin, request, queryset):
    """
    Mark the selected events as featured.

    This admin action updates the 'is_featured' attribute of the provided
    queryset to True. Useful for highlighting important or trending events.

    Parameters:
        modeladmin (ModelAdmin): The current ModelAdmin instance.
        request (HttpRequest): The current HTTP request object.
        queryset (QuerySet): A QuerySet containing the selected objects.
    """
    update_field(queryset, "is_featured", True)


@admin.action(description="Change reservations status to confirmed")
def mark_reservations_confirmed(modeladmin, request, queryset):
    """
    Change the status of selected reservations to Confirmed.

    This admin action sets the 'status' field of the given queryset to
    'Confirmed', indicating that the reservations have been validated and
    approved.

    Parameters:
        modeladmin (ModelAdmin): The current ModelAdmin instance.
        request (HttpRequest): The current HTTP request object.
        queryset (QuerySet): A QuerySet containing the selected objects.
    """
    update_field(queryset, "status", "Confirmed")


@admin.action(description="Change reservations status to Unconfirmed")
def mark_reservations_no_confirmed(modeladmin, request, queryset):
    """
    Change the status of selected reservations to Unconfirmed.

    This admin action sets the 'status' field of the given queryset to
    'Unconfirmed', indicating that the reservations have not been validated
    and are pending approval.

    Parameters:
        modeladmin (ModelAdmin): The current ModelAdmin instance.
        request (HttpRequest): The current HTTP request object.
        queryset (QuerySet): A QuerySet containing the selected objects.
    """
    update_field(queryset, "status", "Unconfirmed")
