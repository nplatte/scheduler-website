import datetime
from turtle import title
from month_view.models import Event
from django.test import TestCase, LiveServerTestCase
from datetime import time, date, datetime
from django.utils import timezone

class TestEvent(TestCase):

    def setUp(self):
        now = datetime.now()
        self.new_event = Event.objects.create(title='test', description='test', time=now.strftime("%H:%M"))

    def test_event_name_is_string(self):
        self.assertIsInstance(self.new_event.title, str)

    def test_event_description_is_string(self):
        self.assertIsInstance(self.new_event.description, str)

    def test_time_format(self):
        self.assertIsInstance(self.new_event.time, str)

    def test_date_format_and_default(self):
        self.assertIsInstance(self.new_event.date, date)
        self.assertEqual(date.today(), self.new_event.date)