from faker import Faker
from rest_framework.test import APITestCase
from event_management.models import Event, Reservation, Attendee, Category, Speaker
from security.models import User, Rol, UserRol
from django.contrib.auth.models import Permission
from django.conf import settings
import jwt
import random
import time

faker = Faker()


class TestSetup(APITestCase):
    """
    Base class for all test cases.
    Provides reusable methods and setup for API tests.
    """

    @classmethod
    def setUpClass(cls):
        """
        Runs once before all test methods in the class.
        Creates permissions, roles, and a default admin user.
        """
        super().setUpClass()
        cls._create_roles()
        cls.category = cls.create_category()
        cls.user = cls._create_user_with_role("Admin")
        cls.token = cls._generate_token(cls.user)

    def setUp(self):
        """
        Runs before each test method.
        Automatically sets the Authorization header for each request.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    @staticmethod
    def _create_roles():
        """
        Create roles and assign appropriate permissions.
        """
        # Crea roles
        admin_role, _ = Rol.objects.get_or_create(name="Admin")
        manager_role, _ = Rol.objects.get_or_create(name="Event Manager")

        # Asigna permisos al rol Admin
        admin_permissions = Permission.objects.filter(
            content_type__app_label="event_management"
        )
        admin_role.permissions.add(*admin_permissions)

        # Asigna permisos específicos al rol Event Manager
        manager_permissions = Permission.objects.filter(
            codename__in=[
                "add_event",
                "view_event",
                "change_event",
                "delete_event",
                "add_reservation",
                "view_reservation",
                "change_reservation",
            ]
        )
        manager_role.permissions.add(*manager_permissions)

    @staticmethod
    def _create_user_with_role(role_name):
        """
        Create a test user and assign a specific role.

        Parameters:
            role_name (str): Name of the role to assign.

        Returns:
            User: The created user.
        """
        user = User.objects.create_user(
            email=faker.email(), password="password123", username=faker.name()
        )
        role = Rol.objects.get(name=role_name)
        UserRol.objects.create(user=user, rol=role, active=True)
        return user

    @staticmethod
    def _generate_token(user):
        """
        Generate a JWT token for the test user.

        Parameters:
            user (User): The user instance for whom the token is generated.

        Returns:
            str: The generated JWT token.
        """
        return jwt.encode(
            {
                "user_id": str(user.id),
                "iat": int(time.time()),
                "exp": int(time.time()) + 3600,  # Expire in 1 hour
            },
            key=settings.SECRET_KEY,
            algorithm="HS256",
        )

    @staticmethod
    def create_category(**kwargs):
        """
        Create a test category.

        Returns:
            Category: The created category instance.
        """
        return Category.objects.create(
            name=kwargs.get("name", faker.word()),
            description=kwargs.get("description", faker.text()),
        )

    def create_event(self, **kwargs):
        """
        Create a test event.

        Returns:
            Event: The created event instance.
        """
        return Event.objects.create(
            name=kwargs.get("name", faker.text(max_nb_chars=20)),
            description=kwargs.get("description", faker.text()),
            date=kwargs.get("date", faker.future_datetime()),
            location=kwargs.get("location", faker.city()),
            total_slots=kwargs.get("total_slots", random.randint(10, 100)),
            category=kwargs.get("category", self.category),
        )

    def create_reservation(self, **kwargs):
        """
        Create a test reservation.

        Returns:
            Reservation: The created reservation instance.
        """
        event = kwargs.get("event", self.create_event())
        attendee = kwargs.get("attendee", self.create_attendee())
        return Reservation.objects.create(
            event=event,
            attendee=attendee,
            reservation_date=kwargs.get("reservation_date", faker.date_time()),
            status=kwargs.get("status", "Pending"),
        )

    def create_attendee(self, **kwargs):
        """
        Create a test attendee.

        Returns:
            Attendee: The created attendee instance.
        """
        return Attendee.objects.create(
            user=kwargs.get("user", self._create_user_with_role("Event Manager"))
        )

    def create_role(self, **kwargs):
        """
        Create a test role.

        Returns:
            Rol: The created role instance.
        """
        return Rol.objects.create(
            name=kwargs.get("name", faker.word()),
            description=kwargs.get("description", faker.text(max_nb_chars=50)),
            active=kwargs.get("active", True),
        )

    def create_speaker(self, **kwargs):
        """
        Create a test speaker.

        Returns:
            Speaker: The created speaker instance.
        """
        return Speaker.objects.create(
            name=kwargs.get("name", faker.name()),
            email=kwargs.get("email", faker.email()),
        )
