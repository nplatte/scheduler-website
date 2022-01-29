from random import choices
import attrs
from django import forms


COLORS = (
            ('red', 'red'),
            ('yellow', 'yellow'),
            ('green', 'green')
        )

class EventForm(forms.Form):
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
    )