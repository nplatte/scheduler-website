from random import choices
import attrs
from django import forms
from django.forms import ModelForm
from .models import Event


COLORS = (
            ('red', 'red'),
            ('yellow', 'yellow'),
            ('green', 'green')
        )

'''class EventForm(forms.Form):
    event_name = forms.CharField(
        widget=forms.fields.TextInput(attrs={
            'class': 'event_name'
        })
        )
    event_color = forms.ChoiceField(
        choices = COLORS,
        widget=forms.Select(attrs={
            'class': 'event_color'
        })
    )
    event_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'class': 'event_time'
        })
    )'''

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'time', 'description']
        widgets = {
            'title': forms.fields.TextInput(attrs={'class': 'event_name'}),
            'time': forms.TimeInput(attrs={'class': 'event_time'})
            }