from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
import month_view.views as views
import month_view.models as models
from django.contrib.auth.models import User
from django.contrib.auth import logout
from datetime import date, datetime


class TestMonthViewPage(LiveServerTestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='test_user', password='password')

    def test_month_view_requires_login(self):
        response = self.client.get(reverse('month_page'), follow=True)
        self.assertTemplateNotUsed(response, 'month_view/month_view.html')

    def test_post_requests_save_model(self):
        self.client.force_login(self.test_user)
        data = {'title': 'topple regime', 'date': date.today()}
        response = self.client.post(reverse('month_page'), data)
        self.assertEqual(1, len(models.Event.objects.all()))

    def test_logout_redirects_to_login_page(self):
        self.client.force_login(self.test_user)
        data = {'logout': ['']}
        response = self.client.post(reverse('month_page'), data, follow=True)
        self.assertTemplateUsed(response, 'login/login.html')

    def test_user_logged_out(self):
        self.client.force_login(self.test_user)
        data = {'logout': ['']}
        response = self.client.post(reverse('month_page'), data)
        logout(self.test_user)
        self.assertFalse(self.test_user.is_authenticated)



class TestHelperFunctions(TestCase):

    def setUp(self):
        self.month = datetime.now().month

    def test_get_month_days(self):
        self.assertEqual(views._get_days_in_month(1, 2022), 31)

    def test_get_events_on_day_returns_list(self):
        models.Event.objects.create(title='New Event', date='2022-01-31')
        events = views._get_events_on_day(31, 1, 2022)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].title, 'New Event')