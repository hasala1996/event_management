import pytest
from core.utils.test_setup import TestSetup
from event_management.models import Reservation
from security.models import Rol


@pytest.mark.django_db
class TestReservationAPI(TestSetup):
    """
    Test cases for Reservation API.
    """

    def setup_method(self, method):
        """
        Setup common elements for each test.
        """
        basic_role, _ = Rol.objects.get_or_create(name="Basic User")
        self.url = "/v1/api/event_management/reservation/"
        self.event = self.create_event(total_slots=10)
        self.attendee = self.create_attendee()
        self.reservation_data = {
            "event": str(self.event.id),
            "attendee": str(self.attendee.id),
            "reservation_date": "2025-05-20T10:00:00Z",
            "status": "Pending",
        }

    def test_create_reservation(self):
        """
        Test creating a reservation.
        """
        response = self.client.post(self.url, self.reservation_data)
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["event"] == self.reservation_data["event"]
        assert response_data["attendee"] == self.reservation_data["attendee"]
        assert response_data["status"] == self.reservation_data["status"]
        assert Reservation.objects.filter(id=response_data["id"]).exists()

    def test_create_reservation_no_slots(self):
        """
        Test creating a reservation for an event with no available slots.
        """
        self.event.total_slots = 0
        self.event.save()

        response = self.client.post(self.url, self.reservation_data)
        assert response.status_code == 400
        response_data = response.json()
        assert response_data["message"] == ["This event has no available slots."]

    def test_list_reservations(self):
        """
        Test listing reservations.
        """
        self.create_reservation(event=self.event, attendee=self.attendee)
        response = self.client.get(self.url)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["count"] == 1
        assert response_data["results"][0]["event_name"] == str(self.event.name)
        assert response_data["results"][0]["attendee_email"] == str(
            self.attendee.user.email
        )

    def test_update_reservation(self):
        """
        Test updating a reservation.
        """
        reservation = self.create_reservation(event=self.event, attendee=self.attendee)
        update_data = {"status": "Confirmed"}

        response = self.client.put(f"{self.url}{reservation.id}/", update_data)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["status"] == update_data["status"]

    def test_delete_reservation(self):
        """
        Test deleting a reservation.
        """
        reservation = self.create_reservation(event=self.event, attendee=self.attendee)
        response = self.client.delete(f"{self.url}{reservation.id}/")
        assert response.status_code == 204
        assert not Reservation.objects.filter(id=reservation.id).exists()

    def test_create_reservation_without_permission(self):
        """
        Test creating a reservation without the required permissions.
        """
        user_without_permission = self._create_user_with_role("Basic User")
        token = self._generate_token(user_without_permission)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.reservation_data)
        response_data = response.json()
        assert response.status_code == 403
        assert response_data["message"] == "Permission denied"
        assert response_data["status"] == 403

    def test_list_reservations_without_permission(self):
        """
        Test listing reservations without the required permissions.
        """
        user_without_permission = self._create_user_with_role("Basic User")
        token = self._generate_token(user_without_permission)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(self.url)
        response_data = response.json()

        assert response.status_code == 403
        assert response_data["message"] == "Permission denied"
        assert response_data["status"] == 403

    def test_update_reservation_without_permission(self):
        """
        Test updating a reservation without the required permissions.
        """
        reservation = self.create_reservation(event=self.event, attendee=self.attendee)

        user_without_permission = self._create_user_with_role("Basic User")
        token = self._generate_token(user_without_permission)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        update_data = {"status": "Confirmed"}
        response = self.client.put(f"{self.url}{reservation.id}/", update_data)
        response_data = response.json()

        assert response.status_code == 403
        assert response_data["message"] == "Permission denied"
        assert response_data["status"] == 403

    def test_delete_reservation_without_permission(self):
        """
        Test deleting a reservation without the required permissions.
        """
        reservation = self.create_reservation(event=self.event, attendee=self.attendee)

        user_without_permission = self._create_user_with_role("Basic User")
        token = self._generate_token(user_without_permission)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete(f"{self.url}{reservation.id}/")
        response_data = response.json()

        assert response.status_code == 403
        assert response_data["message"] == "Permission denied"
        assert response_data["status"] == 403
