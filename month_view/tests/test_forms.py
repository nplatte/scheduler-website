from django.test import TestCase
import month_view.forms as forms


class TestNewEventForm(TestCase):

    def setUp(self):
        self.new_event_form = forms.EventForm()

    def test_title_input_attributes(self):
        form_html = self.new_event_form.as_p()
        self.assertIn('class="event_name"', form_html)
        self.assertIn('maxlength="20"', form_html)
        self.assertIn('required', form_html)

    def test_time_input_attributes(self):
        form_html = self.new_event_form.as_p()
        self.assertIn('class="event_time"', form_html)

    def test_date_input_attributes(self):
        form_html = self.new_event_form.as_p()
        self.assertIn('class="event_date"', form_html)

    def test_description_input_attributes(self):
        form_html = self.new_event_form.as_p()
        self.assertIn('class="event_description"', form_html)
        self.assertIn('maxlength="100"', form_html)