from django.contrib import admin
from .models import User, Rol, UserRol
from .actions import (
    activate_roles,
    deactivate_roles,
    activate_user_roles,
    deactivate_user_roles,
)
from .forms import RolForm, UserRolForm, UserForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin interface for managing User model instances.

    Displays a list of users with their email, status, date joined,
    and associated roles. Allows searching by email and username,
    and filtering by status and date joined.
    """

    form = UserForm
    list_display = ("email", "status", "date_joined", "get_roles", "is_active")
    search_fields = ("email", "username")
    list_filter = ("status", "date_joined", "is_active")
    actions = [activate_roles, deactivate_roles]

    def get_roles(self, obj):
        """
        Retrieve and format the roles associated with a user.

        This method returns a comma-separated string of role names
        assigned to the given User object.

        Parameters:
            obj (User): The user instance being displayed in the admin.

        Returns:
            str: A string containing the names of roles separated by commas.
        """
        return ", ".join([user_rol.rol.name for user_rol in obj.userrol_set.all()])

    get_roles.short_description = "Roles"

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """
        Override the change view to add roles to the context.

        Adds the roles associated with the user to the admin context,
        allowing them to be displayed as read-only in the admin form.

        Parameters:
            request (HttpRequest): The current request object.
            object_id (str): The ID of the user being edited.
            form_url (str): The form URL.
            extra_context (dict): Additional context variables.

        Returns:
            HttpResponse: The response object for the view.
        """
        extra_context = extra_context or {}
        user = self.get_object(request, object_id)
        extra_context["roles"] = self.get_roles(user)
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Rol model instances.

    Displays a list of roles with their name, description, and active status.
    Supports searching by name and description, and filtering by active status.
    Includes actions to activate or deactivate selected roles.
    """

    form = RolForm
    list_display = ("name", "description", "active")
    search_fields = ("name", "description")
    list_filter = ("active",)
    filter_horizontal = ("permissions",)
    actions = [activate_roles, deactivate_roles]


@admin.register(UserRol)
class UserRolAdmin(admin.ModelAdmin):
    """
    Admin interface for managing UserRol model instances.

    Displays a list of user-role associations with user email, role name,
    and active status. Allows searching by user's email and role's name,
    and filtering by active status. Includes actions to activate or
    deactivate selected user roles.
    """

    form = UserRolForm
    list_display = ("user", "rol", "active")
    search_fields = ("user__email", "rol__name")
    list_filter = ("active",)
    actions = [activate_user_roles, deactivate_user_roles]
