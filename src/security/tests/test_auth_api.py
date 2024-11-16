import pytest
from rest_framework import status
from core.utils.test_setup import TestSetup
from security.models import User
from django.contrib.auth.hashers import make_password
from faker import Faker

faker = Faker()


@pytest.mark.django_db
class TestAuthAPI(TestSetup):
    """
    Test cases for the authentication API (login).
    """

    def setup_method(self, method):
        """
        Setup common elements for each test.
        """
        self.url = "/v1/api/auth/login/"
        self.valid_user = self.create_user(
            password="ValidPassword123",
            is_active=True,
        )

    def create_user(self, password, is_active):
        """
        Helper method to create a user.
        """
        return User.objects.create(
            email=faker.email(),
            password=make_password(password),
            is_active=is_active,
            username=faker.name(),
        )

    def test_valid_login(self):
        """
        Test login with valid credentials.
        """
        data = {
            "email": self.valid_user.email,
            "password": "ValidPassword123",
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "token" in response_data
        assert response_data["token"] is not None

    def test_invalid_password(self):
        """
        Test login with an incorrect password.
        """
        data = {
            "email": self.valid_user.email,
            "password": "WrongPassword123",
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        response_data = response.json()
        assert response_data["message"] == "Incorrect email or password"

    def test_nonexistent_user(self):
        """
        Test login with a non-existent user.
        """
        data = {
            "email": "nonexistent@example.com",
            "password": "SomePassword123",
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        response_data = response.json()
        assert response_data["message"] == "Incorrect email or password"

    def test_missing_email_field(self):
        """
        Test login with a missing email field.
        """
        data = {
            "password": "ValidPassword123",
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert "email" in response_data
        assert response_data["email"] == ["This field is required."]

    def test_missing_password_field(self):
        """
        Test login with a missing password field.
        """
        data = {
            "email": self.valid_user.email,
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert "password" in response_data
        assert response_data["password"] == ["This field is required."]
