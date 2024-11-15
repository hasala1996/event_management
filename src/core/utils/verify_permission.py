from functools import wraps
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth.models import Permission
from security.models import UserRol


def verify_permission(permission_codename):
    """
    Decorator to verify if a user has the required permissions for a specific action.

    Parameters:
        permission_codename (str): Codename of the required permission.

    Returns:
        function: The wrapped view function with permission verification.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(instance, request, *args, **kwargs):
            user_id = request.user.id

            if not has_permission_for_action(user_id, permission_codename):
                response = JsonResponse(
                    {
                        "message": "Permission denied",
                        "status": 403,
                        "data": None,
                        "error": "Permission denied",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
                return response

            return view_func(instance, request, *args, **kwargs)

        return _wrapped_view

    return decorator


def has_permission_for_action(user_id, permission_codename):
    """
    Checks if the user has the required permission based on user roles.

    Parameters:
        user_id (UUID): The ID of the user.
        permission_codename (str): Codename of the required permission.

    Returns:
        bool: True if the user has the required permission, False otherwise.
    """

    try:
        user = UserRol.objects.get(user_id=user_id).user

        if user.has_perm(f"{permission_codename}"):
            return True

        permission = Permission.objects.filter(codename=permission_codename).first()
        if not permission:
            return False

        app_label = permission.content_type.app_label

        roles = UserRol.objects.filter(user=user, active=True).values_list(
            "rol", flat=True
        )

        has_permission = Permission.objects.filter(
            roles__id__in=roles,
            content_type__app_label=app_label,
            codename=permission_codename,
        ).exists()

        return has_permission

    except UserRol.DoesNotExist:
        return False
