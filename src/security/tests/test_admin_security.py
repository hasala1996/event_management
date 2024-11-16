import pytest
from django.urls import reverse
from security.models import User, Rol, UserRol
from faker import Faker

faker = Faker()


@pytest.mark.django_db
class TestSecurityAdmin:
    """
    Test cases for the Security app's admin portal.
    """

    @pytest.fixture(autouse=True)
    def setup(self, client):
        """
        Sets up data and logs in as a superuser for admin tests.
        """
        self.client = client
        self.superuser = User.objects.create_superuser(
            email="admin@example.com", password="admin123"
        )
        self.client.login(email="admin@example.com", password="admin123")

        self.role = Rol.objects.create(
            name="Test Role", description="Test Description", active=True
        )
        self.user = User.objects.create_user(
            email="user@example.com", password="user123", username=faker.name()
        )
        self.user_role = UserRol.objects.create(
            user=self.user, rol=self.role, active=True
        )

    def test_role_admin_list_view(self):
        """
        Ensure the list view for roles is accessible and displays correctly.
        """
        url = reverse("admin:security_rol_changelist")
        response = self.client.get(url)
        assert response.status_code == 200
        assert b"Test Role" in response.content

    def test_role_admin_add_view(self):
        """
        Ensure a new role can be added via the admin portal.
        """
        url = reverse("admin:security_rol_add")
        data = {
            "name": "New Role",
            "description": "New Role Description",
            "active": True,
        }
        response = self.client.post(url, data)
        assert response.status_code == 302
        assert Rol.objects.filter(name="New Role").exists()

    def test_role_admin_change_view(self):
        """
        Test updating an existing role via the admin portal.
        """
        url = reverse("admin:security_rol_change", args=[self.role.id])
        data = {
            "name": "Updated Role",
            "description": "Updated Description",
            "active": False,
        }
        response = self.client.post(url, data)
        assert response.status_code == 302
        self.role.refresh_from_db()
        assert self.role.name == "Updated Role"
        assert self.role.active is False

    def test_role_admin_delete_view(self):
        """
        Test deleting a role via the admin portal.
        """
        url = reverse("admin:security_rol_delete", args=[self.role.id])
        response = self.client.post(url, {"post": "yes"})
        assert response.status_code == 302
        assert not Rol.objects.filter(id=self.role.id).exists()

    def test_role_admin_custom_actions(self):
        """
        Test custom actions: activate and deactivate roles.
        """
        url = reverse("admin:security_rol_changelist")
        response = self.client.post(
            url, {"action": "deactivate_roles", "_selected_action": [self.role.id]}
        )
        assert response.status_code == 302
        self.role.refresh_from_db()
        assert self.role.active is False

        response = self.client.post(
            url, {"action": "activate_roles", "_selected_action": [self.role.id]}
        )
        assert response.status_code == 302
        self.role.refresh_from_db()
        assert self.role.active is True

    def test_user_role_admin_list_view(self):
        """
        Ensure the list view for user roles is accessible.
        """
        url = reverse("admin:security_userrol_changelist")
        response = self.client.get(url)
        assert response.status_code == 200
        assert b"Test Role" in response.content

    def test_user_role_admin_custom_actions(self):
        """
        Test activating and deactivating user roles via custom actions.
        """
        url = reverse("admin:security_userrol_changelist")
        response = self.client.post(
            url,
            {
                "action": "deactivate_user_roles",
                "_selected_action": [self.user_role.id],
            },
        )
        assert response.status_code == 302
        self.user_role.refresh_from_db()
        assert self.user_role.active is False

        response = self.client.post(
            url,
            {"action": "activate_user_roles", "_selected_action": [self.user_role.id]},
        )
        assert response.status_code == 302
        self.user_role.refresh_from_db()
        assert self.user_role.active is True

    def test_user_admin_list_view(self):
        """
        Ensure the list view for users is accessible.
        """
        url = reverse("admin:security_user_changelist")
        response = self.client.get(url)
        assert response.status_code == 200
        assert b"user@example.com" in response.content

    def test_user_admin_change_view(self):
        """
        Test updating a user via the admin portal.
        """
        url = reverse("admin:security_user_change", args=[self.user.id])
        data = {
            "email": "updated_user@example.com",
            "username": "updated_username",
            "status": "Active",
            "password": "newpassword123",
            "is_active": True,
        }
        response = self.client.post(url, data)
        assert response.status_code == 302
        self.user.refresh_from_db()
        assert self.user.email == "updated_user@example.com"
