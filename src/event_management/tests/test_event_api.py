import pytest
from core.utils.test_setup import TestSetup
from event_management.models import Event
from security.models import Rol


@pytest.mark.django_db
class TestEventAPI(TestSetup):
    """
    Test cases for Event API.
    """

    def setup_method(self, method):
        """
        Setup common elements for each test.
        """
        basic_role, _ = Rol.objects.get_or_create(name="Basic User")

        self.url = "/v1/api/event_management/event/"
        self.event_data = {
            "name": "Tech Conference",
            "description": "A great tech event.",
            "date": "2025-05-20T10:00:00Z",
            "location": "New York",
            "total_slots": 100,
            "category": self.category.id,
        }

    def test_create_event(self):
        """
        Test creating an event.
        """
        data = {
            "name": "Tech Conference",
            "description": "A great tech event.",
            "date": "2025-05-20T10:00:00Z",
            "location": "New York",
            "category": self.category.id,
        }
        response = self.client.post(self.url, data)
        assert response.status_code == 201
        assert response.data["name"] == data["name"]
        assert response.data["description"] == data["description"]
        assert response.data["category"] == data["category"]
        assert response.data["location"] == data["location"]

        assert Event.objects.filter(name=self.event_data["name"]).exists()

    def test_create_event_invalid_date(self):
        """
        Test creating an event with a date in the past.
        """
        self.event_data["date"] = "2020-01-01T10:00:00Z"
        response = self.client.post(self.url, self.event_data)
        assert response.status_code == 400
        response_data = response.json()
        assert response_data["message"] == "The event date cannot be in the past"

    def test_create_event_missing_data(self):
        """
        Test creating an event with missing fields.
        """
        invalid_data = {
            "name": "Incomplete Event",
        }
        response = self.client.post(self.url, invalid_data)

        assert response.status_code == 400

        expected_errors = {
            "description": ["This field is required."],
            "date": ["This field is required."],
            "location": ["This field is required."],
            "category": ["This field is required."],
        }

        for field, error_message in expected_errors.items():
            assert field in response.data
            assert response.data[field] == error_message

    def test_list_events_with_ordering(self):
        """
        Test listing events with explicit ordering by 'date'.
        Ensures the response matches the order criteria.
        """
        Event.objects.all().delete()

        event_1 = self.create_event(name="Event 1", date="2025-01-01T10:00:00Z")
        event_2 = self.create_event(name="Event 2", date="2025-01-02T10:00:00Z")

        response = self.client.get(f"{self.url}?ordering=date")
        assert response.status_code == 200

        response_data = response.json()
        assert response_data["count"] == 2

        results = response_data["results"]
        assert results[0]["name"] == event_1.name
        assert results[0]["date"] == event_1.date
        assert results[1]["name"] == event_2.name
        assert results[1]["date"] == event_2.date

    def test_list_events_pagination(self):
        """
        Test listing events with pagination.
        Verifies the correct pagination structure and results count.
        """
        for i in range(15):
            self.create_event(name=f"Event {i + 1}")

        response = self.client.get(f"{self.url}?page=1&size=10")
        response_data = response.json()

        assert response.status_code == 200

        assert "count" in response_data
        assert "next" in response_data
        assert "previous" in response_data
        assert "results" in response_data

        assert response_data["count"] == 15
        assert len(response_data["results"]) == 10

        assert (
            response_data["next"]
            == "http://testserver/v1/api/event_management/event/?page=2&size=10"
        )

        assert response_data["previous"] is None

    def test_list_events_search(self):
        """
        Test searching events by name.
        Verifies that only the matching events are returned and validates the paginated response.
        """
        event_1 = self.create_event(name="Tech Conference")
        event_2 = self.create_event(name="Health Conference")

        response = self.client.get(f"{self.url}?search=Tech")
        response_data = response.json()

        assert response.status_code == 200

        assert "count" in response_data
        assert "next" in response_data
        assert "previous" in response_data
        assert "results" in response_data

        assert response_data["count"] == 1
        assert len(response_data["results"]) == 1
        assert response_data["results"][0]["name"] == event_1.name
        assert response_data["results"][0]["id"] == str(event_1.id)

    def test_update_event(self):
        """
        Test updating an event.
        """
        event = self.create_event()
        update_data = {
            "name": "Updated Conference",
            "description": "Updated description",
            "location": "New location Av",
        }
        response = self.client.put(f"{self.url}{event.id}/", update_data)
        assert response.status_code == 200
        assert response.data["name"] == update_data["name"]
        assert response.data["description"] == update_data["description"]

    def test_delete_event(self):
        """
        Test deleting an event.
        """
        event = self.create_event()
        response = self.client.delete(f"{self.url}{event.id}/")
        assert response.status_code == 204
        assert not Event.objects.filter(id=event.id).exists()

    def test_create_event_without_permission(self):
        """
        Test creating an event without the required permissions.
        Verifies that the user receives a 403 Forbidden response.
        """
        user_without_permission = self._create_user_with_role("Basic User")
        token = self._generate_token(user_without_permission)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.event_data)
        response_data = response.json()
        assert response.status_code == 403
        assert response_data["message"] == "Permission denied"
        assert response_data["status"] == 403

    def test_list_events_without_permission(self):
        """
        Test listing events without the required permissions.
        Verifies that the user receives a 403 Forbidden response.
        """
        user_without_permission = self._create_user_with_role("Basic User")
        token = self._generate_token(user_without_permission)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(self.url)
        response_data = response.json()

        assert response.status_code == 403
        assert response_data["message"] == "Permission denied"
        assert response_data["status"] == 403

    def test_update_event_without_permission(self):
        """
        Test updating an event without the required permissions.
        Verifies that the user receives a 403 Forbidden response.
        """
        event = self.create_event()

        user_without_permission = self._create_user_with_role("Basic User")
        token = self._generate_token(user_without_permission)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        update_data = {
            "name": "Unauthorized Update",
            "description": "Should not update",
        }
        response = self.client.put(f"{self.url}{event.id}/", update_data)
        response_data = response.json()

        assert response.status_code == 403
        assert response_data["message"] == "Permission denied"
        assert response_data["status"] == 403

    def test_delete_event_without_permission(self):
        """
        Test deleting an event without the required permissions.
        Verifies that the user receives a 403 Forbidden response.
        """
        event = self.create_event()

        user_without_permission = self._create_user_with_role("Basic User")
        token = self._generate_token(user_without_permission)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete(f"{self.url}{event.id}/")
        response_data = response.json()

        assert response.status_code == 403
        assert response_data["message"] == "Permission denied"
        assert response_data["status"] == 403
