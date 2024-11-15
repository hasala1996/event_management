from django.contrib import admin


def change_active_status(queryset, active_status):
    """
    Generic function to change the 'active' status of the given queryset.

    Parameters:
        queryset (QuerySet): A QuerySet containing the selected objects.
        active_status (bool): The desired status for the 'active' field.
    """
    queryset.update(active=active_status)


@admin.action(description="Activate selected roles")
def activate_roles(self, request, queryset):
    """
    Activate the selected roles.

    This admin action sets the 'active' field of the provided queryset to
    True, indicating that the roles are now active and usable.

    Parameters:
        self (ModelAdmin): The current ModelAdmin instance.
        request (HttpRequest): The current HTTP request object.
        queryset (QuerySet): A QuerySet containing the selected objects.
    """
    change_active_status(queryset, True)


@admin.action(description="Deactivate selected roles")
def deactivate_roles(self, request, queryset):
    """
    Deactivate the selected roles.

    This admin action updates the 'active' attribute of the given queryset
    to False, marking the roles as inactive and unavailable for use.

    Parameters:
        self (ModelAdmin): The current ModelAdmin instance.
        request (HttpRequest): The current HTTP request object.
        queryset (QuerySet): A QuerySet containing the selected objects.
    """
    change_active_status(queryset, False)


@admin.action(description="Activate selected user roles")
def activate_user_roles(self, request, queryset):
    """
    Activate the selected user roles.

    This admin action sets the 'active' field of the provided queryset to
    True, enabling the usage of these specific user roles.

    Parameters:
        self (ModelAdmin): The current ModelAdmin instance.
        request (HttpRequest): The current HTTP request object.
        queryset (QuerySet): A QuerySet containing the selected objects.
    """
    change_active_status(queryset, True)


@admin.action(description="Deactivate selected user roles")
def deactivate_user_roles(self, request, queryset):
    """
    Deactivate the selected user roles.

    This admin action sets the 'active' attribute of the given queryset to
    False, making these specific user roles inactive and not usable.

    Parameters:
        self (ModelAdmin): The current ModelAdmin instance.
        request (HttpRequest): The current HTTP request object.
        queryset (QuerySet): A QuerySet containing the selected objects.
    """
    change_active_status(queryset, False)
