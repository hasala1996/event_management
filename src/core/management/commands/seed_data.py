from django.core.management.base import BaseCommand
from django.utils import timezone
from event_management.models import Category, Speaker, Event, Attendee, Reservation
from django.contrib.auth import get_user_model
import random
from datetime import timedelta

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds the database with initial data for categories, speakers, events, and attendees."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding data..."))

        # Seed categories
        categories = ["Conferencia", "Taller", "Seminario", "Webinar"]
        category_objs = []
        for category_name in categories:
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={"description": f"Descripción de {category_name}"},
            )
            category_objs.append(category)

        self.stdout.write(self.style.SUCCESS("Categories seeded."))

        # Seed speakers
        speakers_data = [
            {
                "name": "Alice Johnson",
                "bio": "Experta en IA.",
                "email": "alice@example.com",
            },
            {
                "name": "Bob Smith",
                "bio": "Desarrollador backend.",
                "email": "bob@example.com",
            },
            {
                "name": "Charlie Brown",
                "bio": "Especialista en datos.",
                "email": "charlie@example.com",
            },
        ]
        speaker_objs = []
        for speaker_data in speakers_data:
            speaker, created = Speaker.objects.get_or_create(
                name=speaker_data["name"],
                defaults={
                    "bio": speaker_data["bio"],
                    "email": speaker_data["email"],
                    "phone_number": f"+12345678{random.randint(10, 99)}",
                },
            )
            speaker_objs.append(speaker)

        self.stdout.write(self.style.SUCCESS("Speakers seeded."))

        # Seed events
        event_objs = []
        base_date = timezone.now()
        for i in range(5):
            event_date = base_date + timedelta(days=i * 7)
            event, created = Event.objects.get_or_create(
                name=f"Evento {i+1}",
                defaults={
                    "description": f"Descripción del evento {i+1}",
                    "date": event_date,
                    "location": f"Ubicación {i+1}",
                    "category": random.choice(category_objs),
                },
            )
            event.speakers.set(
                random.sample(speaker_objs, k=random.randint(1, len(speaker_objs)))
            )
            event_objs.append(event)

        self.stdout.write(self.style.SUCCESS("Events seeded."))

        attendee_objs = []
        for i in range(5):
            user, created = User.objects.get_or_create(
                email=f"attendee{i+1}@example.com",
                first_name=f"attendee{i+1}",
                last_name=f"Apellido{i+1}",
                defaults={"username": f"attendee{i+1}"},
            )
            if created:
                user.set_password("testpassword")
                user.save()
            attendee, created = Attendee.objects.get_or_create(user=user)
            attendee_objs.append(attendee)

        self.stdout.write(self.style.SUCCESS("Attendees seeded."))

        # Seed reservations
        for event in event_objs:
            attendees_for_event = random.sample(
                attendee_objs, k=random.randint(1, len(attendee_objs))
            )
            for attendee in attendees_for_event:
                Reservation.objects.get_or_create(
                    event=event,
                    attendee=attendee,
                    defaults={
                        "reservation_date": timezone.now(),
                        "status": "Confirmed",
                    },
                )

        self.stdout.write(self.style.SUCCESS("Reservations seeded."))
        self.stdout.write(self.style.SUCCESS("Database seeding completed!"))
