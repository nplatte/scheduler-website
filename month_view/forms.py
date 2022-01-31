from random import choices
import attrs
from django import forms
from django.forms import ModelForm
from .models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'time', 'description']
        widgets = {
            'title': forms.fields.TextInput(attrs={'class': 'event_name'}),
            'time': forms.TimeInput(attrs={'class': 'event_time'}),
            'description': forms.Textarea(attrs={'class': 'event_description'})
            }