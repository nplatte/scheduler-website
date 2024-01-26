from django.test import TestCase
from datetime import datetime
from month_view.views import MonthViewPage
from month_view.models import Event

class TestHelperFunctions(TestCase):

    def setUp(self):
        self.month = datetime.now().month
        self.TestClass = MonthViewPage()

    def test_get_month_days(self):
        self.TestClass._set_month_year(1, 2022)
        self.assertEqual(len(self.TestClass._get_days_in_month()), 31)

    def test_get_events_on_day_returns_list(self):
        Event.objects.create(title='New Event', date='2022-01-31')
        events = self.TestClass._get_events_on_day(31, 1, 2022)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].title, 'New Event')

    def test_validate_month_year(self):
        self.TestClass._set_month_year(0, 2022)
        self.TestClass._validate_month_year()
        self.assertEqual(self.TestClass.month, 12)
        self.assertEqual(self.TestClass.year, 2021)
        self.TestClass._set_month_year(13, 2022)
        self.TestClass._validate_month_year()
        self.assertEqual(self.TestClass.month, 1)
        self.assertEqual(self.TestClass.year, 2023)

    def test_get_month_name(self):
        self.TestClass._set_month_year(6, 2022)
        name = self.TestClass._get_month_name()
        self.assertEqual(name, 'June')

    def test_get_day_of_week_month_starts_on(self):
        self.TestClass._set_month_year(6, 2022)
        wednesday = self.TestClass._get_day_of_week_month_starts_on()
        self.assertEqual(3, wednesday)

    def test_get_before_filler_days(self):
        self.TestClass._set_month_year(1, 2022)
        days = self.TestClass._get_before_filler_days(6)
        self.assertEqual(len(days), 6)
        self.assertEqual(days[-1], 31)
    
    def test_get_after_filler_days(self):
        self.TestClass._set_month_year(6, 2022)
        days = self.TestClass._get_after_filler_days()
        self.assertEqual(len(days), 2)
        self.assertEqual([1, 2], days)

    def test_after_does_not_return_days_if_full_week(self):
        self.TestClass._set_month_year(4, 2022)
        days = self.TestClass._get_after_filler_days()
        self.assertNotEqual(7, len(days))
        self.assertEqual(0, len(days))
