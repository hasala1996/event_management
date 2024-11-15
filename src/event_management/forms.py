from django import forms
from django.core.exceptions import ValidationError
from .models import Event
from django.utils import timezone


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "date",
            "location",
            "category",
            "speakers",
            "is_featured",
        ]

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date < timezone.now():
            raise ValidationError("La fecha del evento no puede estar en el pasado.")
        return date

    def clean_speakers(self):
        speakers = self.cleaned_data.get("speakers")
        if speakers and len(speakers) != len(set(speakers)):
            raise ValidationError("Un mismo ponente no puede agregarse más de una vez.")
        return speakers
