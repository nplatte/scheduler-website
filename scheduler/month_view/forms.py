import attrs
from django import forms


class EventForm(forms.Form):
    event_name = forms.CharField(
        widget=forms.fields.TextInput(attrs={
            'class': 'event_name'
        })
        )