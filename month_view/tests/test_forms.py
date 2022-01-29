from django.test import TestCase
import month_view.forms as forms


class TestNewEventForm(TestCase):

    def test_inputs_have_class_names(self):
        new_event_form = forms.EventForm()
        self.assertIn('class="event_name"', new_event_form.as_p())
        self.assertIn('class="event_color"', new_event_form.as_p())
        self.assertIn('class="event_time"', new_event_form.as_p())