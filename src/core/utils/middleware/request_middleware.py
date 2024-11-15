"""
This module contains the RequestMiddleware class, which is used to response errors.
"""

from django.db import IntegrityError
from rest_framework import serializers, status
from rest_framework.response import Response

from core.utils.errors import CustomAPIException


def handle_exception(exc, request):
    if isinstance(exc, serializers.ValidationError):
        return (
            str(exc.detail),
            status.HTTP_400_BAD_REQUEST,
            str(exc.detail.get("error", "Unknown error")),
        )
    elif isinstance(exc, IntegrityError):
        return (
            "Integrity error",
            status.HTTP_400_BAD_REQUEST,
            # str(exc).split("\n", maxsplit=1)[0],
            "INT001",
        )
    elif isinstance(exc, CustomAPIException):
        return (
            str(exc.detail.get("message", ["Unknown error"])[0]),
            exc.status_code,
            str(exc.detail.get("code", "Unknown error")),
        )
    else:
        return str(exc), status.HTTP_400_BAD_REQUEST, "Unhandled exception"


class RegisterRequest:
    """
    Register request class.
    """

    def __init__(self, get_response, *args):
        """
        init method.
        """
        self.get_response = get_response

    def __call__(self, request, **kwargs):
        """capture the request and response the error."""
        try:
            response = self.get_response(request, **kwargs)
        except Exception as e:
            message, status_code, code = handle_exception(e, request)
            response = Response(
                {"message": message, "status": status_code, "code": code},
                status=status_code,
            )

        finally:
            return response
