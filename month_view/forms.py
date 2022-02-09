from random import choices
import attrs
from django import forms
from django.forms import ModelForm
from .models import Event


class NewEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'time', 'description']
        widgets = {
            'title': forms.fields.TextInput(attrs={'class': 'event_title_input', 'id': 'new_event_title'}),
            'time': forms.TimeInput(attrs={'class': 'event_time_input'}),
            'date': forms.DateInput(attrs={'class': 'event_date_input', 'id': 'new_event_date'}),
            'description': forms.Textarea(attrs={'class': 'event_description_input', 'id': 'new_event_description'})
            }


class EditEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'time', 'description']
        widgets = {
            'title': forms.fields.TextInput(attrs={'class': 'edit_event_name', 'id': 'edit_event_name'}),
            'time': forms.TimeInput(attrs={'class': 'edit_event_time'}),
            'date': forms.DateInput(attrs={'class': 'edit_event_date', 'id': 'edit_event_date'}),
            'description': forms.Textarea(attrs={'class': 'edit_event_description'})
            }