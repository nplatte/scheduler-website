from django.test import TestCase
import month_view.forms as forms


class TestNewEventForm(TestCase):

    def setUp(self):
        self.event_form = forms.NewEventForm()

    def test_title_input_attributes(self):
        form_html = self.event_form.as_p()
        self.assertIn('class="event_title_input"', form_html)
        self.assertIn('id="new_event_title"')
        self.assertIn('maxlength="20"', form_html)
        self.assertIn('required', form_html)

    def test_time_input_attributes(self):
        form_html = self.event_form.as_p()
        self.assertIn('class="event_time_input"', form_html)

    def test_date_input_attributes(self):
        form_html = self.event_form.as_p()
        self.assertIn('class="event_date_input"', form_html)
        self.assertIn('id="new_event_date"', form_html)

    def test_description_input_attributes(self):
        form_html = self.event_form.as_p()
        self.assertIn('class="event_description_input"', form_html)
        self.assertIn('id="new_event_description"', form_html)
        self.assertIn('maxlength="100"', form_html)


class TestEditEventForm(TestCase):

    def setUp(self):
        self.event_form = forms.EditEventForm()

    def test_title_input_attributes(self):
        form_html = self.event_form.as_p()
        self.assertIn('class="event_title_input"', form_html)
        self.assertIn('id="edit_event_title"', form_html)
        self.assertIn('maxlength="20"', form_html)
        self.assertIn('required', form_html)

    def test_time_input_attributes(self):
        form_html = self.event_form.as_p()
        self.assertIn('class="event_time_input"', form_html)

    def test_date_input_attributes(self):
        form_html = self.event_form.as_p()
        self.assertIn('class="event_date_input"', form_html)
        self.assertIn('id="edit_event_date"', form_html)

    def test_description_input_attributes(self):
        form_html = self.event_form.as_p()
        self.assertIn('class="event_description_input"', form_html)
        self.assertIn('id="edit_event_description"', form_html)
        self.assertIn('maxlength="100"', form_html)