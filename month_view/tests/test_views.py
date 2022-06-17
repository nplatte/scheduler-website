from urllib import response
from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
from month_view.views import MonthViewPage
import month_view.models as models
import month_view.forms as forms
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

    def test_get_returns_200_status_code(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('month_page', kwargs={'month': 2, 'year': 2022}), follow=True)
        self.assertEqual(200, response.status_code)


class TestLogoutPOST(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='test_user', password='password')
        self.client.force_login(self.test_user)
        self.data = {'logout': ['']}

    def test_logout_redirects_to_login_page(self):
        response = self.client.post(reverse('month_page', kwargs={'month': 2, 'year': 2022}), self.data, follow=True)
        self.assertTemplateUsed(response, 'login/login.html')

    def test_user_logged_out(self):
        response = self.client.post(reverse('month_page', kwargs={'month': 2, 'year': 2022}), self.data, follow=True)
        self.assertTemplateNotUsed(response, 'month_view/month_view.html')


class TestRightArrowPOST(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='test_user', password='password')
        self.client.force_login(self.test_user)
        self.data = {'right_month': ['']}

    def test_right_arrow_post_uses_template(self):
        response = self.client.post(reverse('month_page', kwargs={'month': 2, 'year': 2022}), self.data, follow=True)
        self.assertTemplateUsed(response, 'month_view/month_view.html')

    def test_right_arrow_context_returns_month_plus_one(self):
        response = self.client.post(reverse('month_page', kwargs={'month': 2, 'year': 2022}), self.data, follow=True)
        self.assertEqual(3, response.context['month_number'])

    def test_year_number_goes_up_on_december_right_month(self):
        response = self.client.post(reverse('month_page', kwargs={'month': 12, 'year': 2022}), self.data, follow=True)
        self.assertEqual(2023, response.context['year_number'])

    def test_month_day_info_is_of_next_month(self):
        response = self.client.post(reverse('month_page', kwargs={'month': 6, 'year': 2022}), self.data, follow=True)
        self.assertNotEqual(30, len(response.context['month_events']))
        self.assertEqual(31, len(response.context['month_events']))

    def test_right_month_redirects_to_month_view(self):
        response = self.client.post(reverse('month_page', kwargs={'month': 1, 'year': 2022}), self.data, follow=True)
        self.assertRedirects(response, '/month_view/2-2022/')


class TestLeftArrowPOST(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='test_user', password='password')
        self.client.force_login(self.test_user)
        self.data = {'left_month': ['']}

    def test_right_arrow_post_uses_template(self):
        response = self.client.post(reverse('month_page', kwargs={'month': 2, 'year': 2022}), self.data, follow=True)
        self.assertTemplateUsed(response, 'month_view/month_view.html')

    def test_left_arrow_context_returns_month_minus_one(self):
        response = self.client.post(reverse('month_page', kwargs={'month': 2, 'year': 2022}), self.data, follow=True)
        self.assertEqual(1, response.context['month_number'])

    def test_year_number_goes_down_on_december_left_month(self):
        response = self.client.post(reverse('month_page', kwargs={'month': 1, 'year': 2022}), self.data, follow=True)
        self.assertEqual(2021, response.context['year_number'])

    def test_month_day_info_is_of_last_month(self):
        response = self.client.post(reverse('month_page', kwargs={'month': 6, 'year': 2022}), self.data, follow=True)
        self.assertNotEqual(30, len(response.context['month_events']))
        self.assertEqual(31, len(response.context['month_events']))

    def test_left_month_redirects_to_month_view(self):
        response = self.client.post(reverse('month_page', kwargs={'month': 1, 'year': 2022}), self.data, follow=True)
        self.assertRedirects(response, '/month_view/12-2021/')


class TestNewEventPost(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='test_user', password='password')
        self.client.force_login(self.test_user)

    def test_post_creates_new_event(self):
        data = {'new_event': [], 'title': 'topple regime', 'date': date.today()}
        response = self.client.post(reverse('month_page', kwargs={'month': 2, 'year': 2022}), data)
        self.assertEqual(1, len(models.Event.objects.all()))

    def test_post_sends_date(self):
        data = {'new_event': [], 'title': 'topple regime', 'date': date.today()}
        response = self.client.post(reverse('month_page', kwargs={'month': 2, 'year': 2022}), data)
        self.assertEqual(2, response.context['month_number'])
        self.assertEqual(2022, response.context['year_number'])

    def test_post_sends_event_to_html(self):
        data = {'new_event': [], 'title': 'topple regime', 'date': date(2022, 2, 1)}
        response = self.client.post(reverse('month_page', kwargs={'month': 2, 'year': 2022}), data)
        self.assertEqual(1, len(models.Event.objects.all()))
        self.assertEqual(2, len(response.context['month_events'][0]))
        self.assertEqual(1, len(response.context['month_events'][0][1]))


class TestEditEventPOST(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='test_user', password='password')
        self.client.force_login(self.test_user)

    def test_post_request_with_edit_event_updates_event(self):
        event = models.Event.objects.create(title='Topple Regime', description='they goin down', date=date.today())
        data = {
            'edit_event': [''],
            'event_id': event.pk,
            'title': "don't topple regime",
            'date': date.today(),
            'description': 'we done fucked up'
        }
        response = self.client.post(reverse('month_page', kwargs={'month':2, 'year': 2022}), data)
        self.assertEqual(len(models.Event.objects.all()), 1)
        self.assertEqual("don't topple regime", models.Event.objects.all()[0].title)


class TestDeleteEventPOST(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='test_user', password='password')
        self.client.force_login(self.test_user)

    def test_post_deletes_event(self):
        event = models.Event.objects.create(title='Topple Regime', description='they goin down', date=date.today())
        data = {
            'delete_event': [''],
            'event_id': event.pk,
        }
        response = self.client.post(reverse('month_page', kwargs={'month':2, 'year': 2022}), data)
        self.assertEqual(len(models.Event.objects.all()), 0)


class TestHelperFunctions(TestCase):

    def setUp(self):
        self.month = datetime.now().month
        self.TestClass = MonthViewPage()

    def test_get_month_days(self):
        self.TestClass._set_month_year(1, 2022)
        self.assertEqual(len(self.TestClass._get_days_in_month()), 31)

    def test_get_events_on_day_returns_list(self):
        models.Event.objects.create(title='New Event', date='2022-01-31')
        events = self.TestClass._get_events_on_day(31, 1, 2022)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].title, 'New Event')

    '''def test_get_dates_in_month_returns_days_for_full_month(self):
        dates_in_month = views._get_dates_in_month(2, 2022)
        self.assertEqual(28, len(dates_in_month))
        date_parts = dates_in_month[0].split('-')
        self.assertEqual('2022', date_parts[0])
        self.assertEqual('2', date_parts[1])
        self.assertEqual('1', date_parts[2])'''

    def test_validate_month_year(self):
        self.TestClass._set_month_year(0, 2022)
        month, year = self.TestClass._validate_month_year()
        self.assertEqual(month, 12)
        self.assertEqual(year, 2021)
        self.TestClass._set_month_year(13, 2022)
        month, year = self.TestClass._validate_month_year()
        self.assertEqual(month, 1)
        self.assertEqual(year, 2023)

    def test_get_month_name(self):
        self.TestClass._set_month_year(6, 2022)
        name = self.TestClass._get_month_name()
        self.assertEqual(name, 'June')

    '''def test_get_day_of_week_month_starts_on(self):
        tuesday = views._get_day_of_week_month_starts_on(2, 2022)
        self.assertEqual(2, tuesday)

    def test_get_before_filler_days(self):
        days = views._get_before_filler_days(6, 1, 2022)
        self.assertEqual(len(days), 6)
        self.assertEqual(days[-1], 31)
    
    def test_get_after_filler_days(self):
        days = views._get_after_filler_days(1, 1, 2022)
        self.assertEqual(len(days), 5)
        self.assertEqual(days[-1], 5)'''

