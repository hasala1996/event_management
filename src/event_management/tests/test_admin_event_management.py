import pytest
from django.urls import reverse
from event_management.models import Event
from core.utils.test_setup import TestSetup
from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestEventManagementAdmin(TestSetup):
    """
    Test cases for the Event Management app's admin portal.
    """

    def setUp(self):
        """
        Set up additional data and log in as a superuser for admin tests.
        """
        super().setUp()

        self.superuser = get_user_model().objects.create_superuser(
            email="admin@example.com", password="admin123"
        )
        self.client.login(email="admin@example.com", password="admin123")
        self.category = self.create_category(name="Tech", description="Tech Events")
        self.event = self.create_event(name="Test Event", category=self.category)
        self.attendee = self.create_attendee()
        self.reservation = self.create_reservation(
            event=self.event, attendee=self.attendee
        )
        self.speaker = self.create_speaker()

    def test_event_admin_list_view(self):
        """
        Ensure the list view for events is accessible and displays correct data.
        """
        url = reverse("admin:event_management_event_changelist")
        response = self.client.get(url)
        assert response.status_code == 200
        assert b"Test Event" in response.content
        assert b"Tech" in response.content

    def test_event_admin_add_view(self):
        """
        Ensure a new event can be added via the admin portal.
        """
        url = reverse("admin:event_management_event_add")

        self.client.get(url)

        data = {
            "name": "New Event",
            "description": "New Event Description",
            "date_0": "2025-01-01",
            "date_1": "10:00:00",
            "location": "New York",
            "category": self.category.id,
            "is_featured": False,
            "speakers": str(self.speaker.id),
        }
        response = self.client.post(url, data)
        print(response.content.decode())

        assert response.status_code == 302
        assert Event.objects.filter(name="New Event").exists()

    def test_event_admin_change_view(self):
        """
        Test updating an event via the admin portal.
        """
        url = reverse("admin:event_management_event_change", args=[self.event.id])
        data = {
            "name": "Updated Event",
            "description": "Updated Description",
            "date_0": "2025-01-01",
            "date_1": "10:00:00",
            "location": "Updated Location",
            "category": self.category.id,
            "is_featured": True,
            "speakers": str(self.speaker.id),
        }
        response = self.client.post(url, data)
        assert response.status_code == 302
        self.event.refresh_from_db()
        assert self.event.name == "Updated Event"
        assert self.event.is_featured is True

    def test_event_admin_delete_view(self):
        """
        Test deleting an event via the admin portal.
        """
        url = reverse("admin:event_management_event_delete", args=[self.event.id])
        response = self.client.post(url, {"post": "yes"})
        assert response.status_code == 302
        assert not Event.objects.filter(id=self.event.id).exists()

    def test_event_admin_custom_action_featured(self):
        """
        Test marking events as featured using the custom action.
        """
        url = reverse("admin:event_management_event_changelist")
        response = self.client.post(
            url, {"action": "make_events_featured", "_selected_action": [self.event.id]}
        )
        assert response.status_code == 302
        self.event.refresh_from_db()
        assert self.event.is_featured is True

    def test_reservation_admin_list_view(self):
        """
        Ensure the list view for reservations is accessible and displays correct data.
        """
        url = reverse("admin:event_management_reservation_changelist")
        response = self.client.get(url)
        assert response.status_code == 200
        assert b"Test Event" in response.content
        assert self.attendee.user.email.encode() in response.content

    def test_reservation_admin_custom_action_confirmed(self):
        """
        Test marking reservations as confirmed using the custom action.
        """
        url = reverse("admin:event_management_reservation_changelist")
        response = self.client.post(
            url,
            {
                "action": "mark_reservations_confirmed",
                "_selected_action": [self.reservation.id],
            },
        )
        assert response.status_code == 302
        self.reservation.refresh_from_db()
        assert self.reservation.status == "Confirmed"

    def test_reservation_admin_custom_action_unconfirmed(self):
        """
        Test marking reservations as unconfirmed using the custom action.
        """
        url = reverse("admin:event_management_reservation_changelist")
        response = self.client.post(
            url,
            {
                "action": "mark_reservations_no_confirmed",
                "_selected_action": [self.reservation.id],
            },
        )
        assert response.status_code == 302
        self.reservation.refresh_from_db()
        assert self.reservation.status == "Unconfirmed"
