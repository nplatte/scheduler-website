from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
import month_view.views as views
import month_view.models as models
from django.contrib.auth.models import User
from datetime import date, datetime

from functional_test.test import _get_month_name

class TestMonthViewPage(LiveServerTestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='test_user', password='password')

    def test_month_view_uses_right_template(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('month_page', kwargs={'month': 2, 'year': 2022}), follow=True)
        self.assertTemplateUsed(response, 'month_view/month_view.html')

    def test_month_view_requires_login(self):
        response = self.client.get(reverse('month_page', kwargs={'month': 2, 'year': 2022}), follow=True)
        self.assertTemplateNotUsed(response, 'month_view/month_view.html')

    def test_post_requests_save_model(self):
        self.client.force_login(self.test_user)
        data = {'title': 'topple regime', 'date': date.today()}
        response = self.client.post(reverse('month_page', kwargs={'month': 2, 'year': 2022}), data)
        self.assertEqual(1, len(models.Event.objects.all()))


class TestMonthViewArrows(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='test_user', password='password')

    def test_logout_redirects_to_login_page(self):
        self.client.force_login(self.test_user)
        data = {'logout': ['']}
        response = self.client.post(reverse('month_page', kwargs={'month': 2, 'year': 2022}), data, follow=True)
        self.assertTemplateUsed(response, 'login/login.html')

    def test_user_logged_out(self):
        self.client.force_login(self.test_user)
        data = {'logout': ['']}
        response = self.client.post(reverse('month_page', kwargs={'month': 2, 'year': 2022}), data, follow=True)
        self.assertTemplateNotUsed(response, 'month_view/month_view.html')

    def test_right_arrow_post_uses_template(self):
        self.client.force_login(self.test_user)
        data = {'right_month': ['']}
        response = self.client.post(reverse('month_page', kwargs={'month': 2, 'year': 2022}), data, follow=True)
        self.assertTemplateUsed(response, 'month_view/month_view.html')

    def test_right_arrow_context_returns_non_curent_month_name(self):
        self.client.force_login(self.test_user)
        data = {'right_month': ['']}
        response = self.client.post(reverse('month_page', kwargs={'month': 2, 'year': 2022}), data, follow=True)
        self.assertTemplateUsed(response, 'month_view/month_view.html')
        self.assertNotEqual(response.context['month_name'], _get_month_name())

    def test_left_arrow_context_returns_month_minus_one(self):
        self.client.force_login(self.test_user)
        data = {'left_month': ['']}
        response = self.client.post(reverse('month_page', kwargs={'month': 2, 'year': 2022}), data, follow=True)
        self.assertEqual(1, response.context['month_number'])

    def test_year_number_goes_up_on_december_right_month(self):
        self.client.force_login(self.test_user)
        data = {'right_month': ['']}
        response = self.client.post(reverse('month_page', kwargs={'month': 12, 'year': 2022}), data, follow=True)
        self.assertEqual(2023, response.context['year_number'])
    
    def test_year_number_goes_up_on_december_left_month(self):
        self.client.force_login(self.test_user)
        data = {'left_month': ['']}
        response = self.client.post(reverse('month_page', kwargs={'month': 1, 'year': 2022}), data, follow=True)
        self.assertEqual(2021, response.context['year_number'])

    def test_left_month_redirects_to_month_view(self):
        self.client.force_login(self.test_user)
        data = {'left_month': ['']}
        response = self.client.post(reverse('month_page', kwargs={'month': 1, 'year': 2022}), data, follow=True)
        self.assertRedirects(response, 'month_view/12-2021/')


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

    def test_get_dates_in_month_returns_days_for_full_month(self):
        dates_in_month = views._get_dates_in_month(2, 2022)
        self.assertEqual(28, len(dates_in_month))
        date_parts = dates_in_month[0].split('-')
        self.assertEqual('2022', date_parts[0])
        self.assertEqual('2', date_parts[1])
        self.assertEqual('1', date_parts[2])
