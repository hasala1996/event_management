"""
This file contains the permission class for the authorizer.
"""

import logging
import jwt
from rest_framework.permissions import BasePermission
from django.conf import settings
from security.models import User
from core.utils.errors import APIErrors, CustomAPIException

logger = logging.getLogger(__name__)


class AuthorizerPermission(BasePermission):
    """
    Permission class to authorize users based on JWT tokens in the Authorization header.
    """

    def has_permission(self, request, view):
        """
        Checks if the user has permission based on the JWT token in the Authorization header.

        Parameters:
            request (HttpRequest): The current request instance.
            view (View): The view instance being accessed.

        Returns:
            bool: True if the user has permission, otherwise raises a CustomAPIException.
        """
        token = self._get_token_from_header(request)

        try:
            payload = jwt.decode(
                jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = payload.get("user_id")

            if not user_id:
                raise CustomAPIException(
                    detail=APIErrors.INVALID_AUTH_TOKEN["message"],
                    code=APIErrors.INVALID_AUTH_TOKEN["code"],
                )

            request.user = self._get_user(user_id)

        except jwt.ExpiredSignatureError:
            raise CustomAPIException(
                detail=APIErrors.EXPIRED_AUTH_TOKEN["message"],
                code=APIErrors.EXPIRED_AUTH_TOKEN["code"],
            )
        except jwt.InvalidTokenError:
            raise CustomAPIException(
                detail=APIErrors.INVALID_AUTH_TOKEN["message"],
                code=APIErrors.INVALID_AUTH_TOKEN["code"],
            )
        except Exception as e:
            logger.error("Unexpected error during token processing: %s", e)
            raise CustomAPIException(
                detail=APIErrors.SERVER_ERROR["message"],
                code=APIErrors.SERVER_ERROR["code"],
            )

        return True

    def _get_token_from_header(self, request):
        """
        Extracts the JWT token from the Authorization header.

        Parameters:
            request (HttpRequest): The current request instance.

        Returns:
            str: The JWT token if present and correctly formatted.

        Raises:
            CustomAPIException: If the token is missing or not in the correct format.
        """
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise CustomAPIException(
                detail=APIErrors.INVALID_AUTH_TOKEN["message"],
                code=APIErrors.INVALID_AUTH_TOKEN["code"],
            )
        return auth_header.split(" ")[1]

    def _get_user(self, user_id):
        """
        Retrieves the user instance by user_id.

        Parameters:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The user instance.

        Raises:
            CustomAPIException: If the user does not exist.
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise CustomAPIException(
                detail=APIErrors.RESOURCE_NOT_FOUND["message"],
                code=APIErrors.RESOURCE_NOT_FOUND["code"],
            )
