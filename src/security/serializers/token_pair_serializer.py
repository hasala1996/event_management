from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings
from core.utils.errors import AuthErrors, CustomAPIException


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer to obtain token for a user with added custom validations.
    Includes additional fields in the token and validates user account status.
    """

    @classmethod
    def get_token(cls, user):
        """
        Customizes the JWT token by adding the user's last login time.

        Parameters:
            user (User): The user instance for whom the token is generated.

        Returns:
            token (Token): The customized token with additional claims.
        """
        token = super().get_token(user)

        if user.last_login:
            token["last_login"] = user.last_login.strftime("%Y/%m/%d - %H:%M:%S")

        user.last_login = datetime.now()
        user.save()

        return token

    def validate(self, attrs):
        """
        Validates user credentials and account status. Generates JWT token if valid.

        Parameters:
            attrs (dict): Contains the username and password provided by the user.

        Raises:
            CustomAPIException: If authentication fails or account is inactive.

        Returns:
            dict: Contains the access token.
        """
        self.user = self._authenticate_user(attrs)

        self._validate_user_status(self.user)

        token = self.get_token(self.user)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return {"token": str(token.access_token)}

    def _authenticate_user(self, attrs):
        """
        Authenticates the user using provided credentials.

        Parameters:
            attrs (dict): Contains the username and password.

        Returns:
            User: The authenticated user.

        Raises:
            CustomAPIException: If authentication fails.
        """
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }

        if "request" in self.context:
            authenticate_kwargs["request"] = self.context["request"]

        user = authenticate(**authenticate_kwargs)

        if user is None:
            raise CustomAPIException(
                detail=AuthErrors.INVALID_EMAIL_PASSWORD["message"],
                code=AuthErrors.INVALID_EMAIL_PASSWORD["code"],
            )

        return user

    def _validate_user_status(self, user):
        """
        Validates if the user account is active.

        Parameters:
            user (User): The user instance.

        Raises:
            CustomAPIException: If the user account is inactive.
        """
        if not user.is_active:
            raise CustomAPIException(
                detail=AuthErrors.INACTIVE_ACCOUNT["message"],
                code=AuthErrors.INACTIVE_ACCOUNT["code"],
            )
