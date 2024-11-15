from rest_framework.exceptions import APIException


class CustomAPIException(APIException):
    status_code = 400

    def __init__(self, detail, code):
        super().__init__(detail)
        self.detail = {
            "message": [detail],
            "status": code,
            "data": None,
            "code": code,
        }


class APIErrors:
    INVALID_AUTH_TOKEN = {
        "code": "API001",
        "message": "Invalid authentication token",
    }
    RESOURCE_NOT_FOUND = {"code": "API002", "message": "Resource not found"}
    INVALID_REQUEST_FORMAT = {
        "code": "API003",
        "message": "Invalid request format",
    }
    SERVER_ERROR = {"code": "API004", "message": "Internal server error"}
    UNAUTHORIZED_ACCESS = {"code": "API005", "message": "Unauthorized access"}
    EXPIRED_AUTH_TOKEN = {
        "code": "API006",
        "message": "Expired authentication token, please log in again",
    }
    INVALID_REQUEST = {
        "code": "API007",
        "message": "Cannot delete a role that is in use",
    }


class FormErrors:
    REQUIRED_FIELD_MISSING = {
        "code": "FORM001",
        "message": "Required field missing",
    }
    INVALID_EMAIL_FORMAT = {
        "code": "FORM002",
        "message": "Invalid email format",
    }
    PASSWORD_LENGTH_ERROR = {
        "code": "FORM003",
        "message": "Password must contain at least 8 characters",
    }
    PASSWORD_MISMATCH = {"code": "FORM004", "message": "Passwords do not match"}
    INVALID_DATE_FORMAT = {"code": "FORM005", "message": "Invalid date format"}
    INVALID_ID = {"code": "FORM006", "message": "Invalid ID"}
    INVALID_DATA_TYPE = {"code": "FORM007", "message": "Invalid data type"}
    INVALID_DATE = {
        "code": "FORM008",
        "message": "The event date cannot be in the past",
    }
    DUPLICATE_RESERVATION = {
        "code": "FORM009",
        "message": "You already have a reservation for this event.",
    }


class AuthErrors:
    INVALID_EMAIL_PASSWORD = {
        "code": "AUTH001",
        "message": "Incorrect email or password",
    }
    NOT_FOUND_EMAIL = {"code": "AUTH002", "message": "Email not found"}
    INVALID_PASSWORD = {"code": "AUTH003", "message": "The password is not valid"}
    EMAIL_EXISTS = {"code": "AUTH004", "message": "Email already exists"}
    INACTIVE_ACCOUNT = {"code": "AUTH005", "message": "Inactive user"}
    INVALID_ROLE = {"code": "AUTH006", "message": "Invalid role"}


class HttpErrors:
    NOT_FOUND = {"code": "404", "message": "Not found"}
    BAD_REQUEST = {"code": "400", "message": "Bad request"}
    INTERNAL_SERVER_ERROR = {"code": "500", "message": "Internal server error"}
    SERVICE_UNAVAILABLE = {"code": "503", "message": "Service unavailable"}
    GATEWAY_TIMEOUT = {
        "code": "504",
        "message": "Gateway timeout while trying to access the resource",
    }
