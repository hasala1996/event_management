import jwt
import pytest
from unittest.mock import MagicMock, patch
from security.models import User
from core.utils.errors import CustomAPIException, APIErrors
from core.utils.authorizer_permission import AuthorizerPermission


@pytest.mark.django_db
class TestAuthorizerPermission:
    """
    Test cases for the AuthorizerPermission class.
    """

    def setup_method(self):
        """
        Setup common elements for the tests.
        """
        self.permission = AuthorizerPermission()
        self.valid_token = "valid.jwt.token"
        self.expired_token = "expired.jwt.token"
        self.invalid_token = "invalid.jwt.token"
        self.user = User.objects.create_user(
            email="user@example.com", password="password123"
        )
        self.payload = {"user_id": str(self.user.id)}

    def test_missing_authorization_header(self):
        """
        Test when the Authorization header is missing.
        """
        request = MagicMock()
        request.headers = {}

        with pytest.raises(CustomAPIException) as exc:
            self.permission.has_permission(request, None)

        exc_value = exc.value
        assert exc_value.detail["message"] == "Invalid authentication token"
        assert exc_value.detail["code"] == "API001"

    def test_invalid_authorization_format(self):
        """
        Test when the Authorization header has an invalid format.
        """
        request = MagicMock()
        request.headers = {"Authorization": "InvalidFormat"}

        with pytest.raises(CustomAPIException) as exc:
            self.permission.has_permission(request, None)
        exc_value = exc.value
        assert exc_value.detail["message"] == APIErrors.INVALID_AUTH_TOKEN["message"]
        assert exc_value.detail["code"] == APIErrors.INVALID_AUTH_TOKEN["code"]

    @patch("jwt.decode")
    def test_expired_token(self, mock_jwt_decode):
        """
        Test when the token is expired.
        """
        mock_jwt_decode.side_effect = jwt.ExpiredSignatureError
        request = MagicMock()
        request.headers = {"Authorization": f"Bearer {self.expired_token}"}

        with pytest.raises(CustomAPIException) as exc:
            self.permission.has_permission(request, None)

        exc_value = exc.value
        assert exc_value.detail["message"] == APIErrors.EXPIRED_AUTH_TOKEN["message"]
        assert exc_value.detail["code"] == APIErrors.EXPIRED_AUTH_TOKEN["code"]

    @patch("jwt.decode")
    def test_invalid_token(self, mock_jwt_decode):
        """
        Test when the token is invalid.
        """
        mock_jwt_decode.side_effect = jwt.InvalidTokenError
        request = MagicMock()
        request.headers = {"Authorization": f"Bearer {self.invalid_token}"}

        with pytest.raises(CustomAPIException) as exc:
            self.permission.has_permission(request, None)

        exc_value = exc.value
        assert exc_value.detail["message"] == APIErrors.INVALID_AUTH_TOKEN["message"]
        assert exc_value.detail["code"] == APIErrors.INVALID_AUTH_TOKEN["code"]

    @patch("core.utils.authorizer_permission.jwt.decode")
    @patch("core.utils.authorizer_permission.User.objects.get")
    def test_valid_token(self, mock_get_user, mock_jwt_decode):
        """
        Test when the token is valid.
        """
        mock_jwt_decode.return_value = self.payload
        mock_get_user.return_value = self.user
        request = MagicMock()
        request.headers = {"Authorization": f"Bearer {self.valid_token}"}

        assert self.permission.has_permission(request, None) is True
        assert request.user == self.user

    @patch("core.utils.authorizer_permission.jwt.decode")
    @patch("core.utils.authorizer_permission.User.objects.get")
    def test_unexpected_error(self, mock_get_user, mock_jwt_decode):
        """
        Test an unexpected error during token processing.
        """
        mock_jwt_decode.side_effect = Exception("Unexpected error")
        request = MagicMock()
        request.headers = {"Authorization": f"Bearer {self.valid_token}"}

        with pytest.raises(CustomAPIException) as exc:
            self.permission.has_permission(request, None)

        exc_value = exc.value
        assert exc_value.detail["message"] == APIErrors.SERVER_ERROR["message"]
        assert exc_value.detail["code"] == APIErrors.SERVER_ERROR["code"]
