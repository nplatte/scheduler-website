from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models import User
from month_view.models import Event
from month_view.forms import NewEventForm, EditEventForm
from django.urls import reverse
from datetime import date


class TestViewPOSTContext(LiveServerTestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='test_user', password='password')
        self.client.force_login(self.test_user)
        view_data = {'month': 2, 'year': 2022}
        event = Event.objects.create(title='Topple Regime', description='they goin down', date=date.today())
        post_data = {
            'delete_event': [''],
            'event_id': event.pk,
        }
        self.response = self.client.post(reverse('month_page', kwargs=view_data), post_data)

    def test_get_context_new_event_form(self):
        self.assertIsInstance(self.response.context['new_form'], NewEventForm)

    def test_get_context_edit_event_form(self):
        self.assertIsInstance(self.response.context['edit_form'], EditEventForm)

    def test_get_context_month_name(self):
        self.assertEqual('February', self.response.context['month_name'])

    def test_get_context_month_and_year_number(self):
        self.assertEqual(2, self.response.context['month_number'])
        self.assertEqual(2022, self.response.context['year_number'])

    def test_get_context_month_events_in_right_format(self):
        self.assertEqual(len(self.response.context['month_events']), 28)
        self.assertIsInstance(self.response.context['month_events'][0][1], list)

    def test_get_context_last_month_events_in_right_format(self):
        self.assertEqual(len(self.response.context['last_month_events']), 2)
        self.assertIsInstance(self.response.context['month_events'][0][1], list)

    def test_get_context_next_month_events_in_right_format(self):
        self.assertEqual(len(self.response.context['next_month_events']), 5)
        self.assertIsInstance(self.response.context['month_events'][0][1], list)

    def test_total_month_event_lens_divids_7(self):
        last_month_events = self.response.context['last_month_events']
        this_month_events = self.response.context['month_events']
        next_month_events = self.response.context['next_month_events']
        total_event_list = last_month_events + this_month_events + next_month_events
        self.assertEqual(len(total_event_list), 35)


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


class TestNewEventPost(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='test_user', password='password')
        self.client.force_login(self.test_user)

    def test_post_creates_new_event(self):
        data = {'new_event': [], 'title': 'topple regime', 'date': date.today()}
        response = self.client.post(reverse('month_page', kwargs={'month': 2, 'year': 2022}), data)
        self.assertEqual(1, len(Event.objects.all()))

    def test_post_sends_date(self):
        data = {'new_event': [], 'title': 'topple regime', 'date': date.today()}
        response = self.client.post(reverse('month_page', kwargs={'month': 2, 'year': 2022}), data)
        self.assertEqual(2, response.context['month_number'])
        self.assertEqual(2022, response.context['year_number'])

    def test_post_sends_event_to_html(self):
        data = {'new_event': [], 'title': 'topple regime', 'date': date(2022, 2, 1)}
        response = self.client.post(reverse('month_page', kwargs={'month': 2, 'year': 2022}), data)
        self.assertEqual(1, len(Event.objects.all()))
        self.assertEqual(2, len(response.context['month_events'][0]))
        self.assertEqual(1, len(response.context['month_events'][0][1]))


class TestEditEventPOST(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='test_user', password='password')
        self.client.force_login(self.test_user)

    def test_post_request_with_edit_event_updates_event(self):
        event = Event.objects.create(title='Topple Regime', description='they goin down', date=date.today())
        data = {
            'edit_event': [''],
            'event_id': event.pk,
            'title': "don't topple regime",
            'date': '2022-02-22',
            'description': 'we done fucked up'
        }
        response = self.client.post(reverse('month_page', kwargs={'month':2, 'year': 2022}), data)
        self.assertEqual(len(Event.objects.all()), 1)
        self.assertEqual("don't topple regime", Event.objects.all()[0].title)
        self.assertEqual('2022-02-22' , str(Event.objects.all()[0].date))


class TestDeleteEventPOST(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='test_user', password='password')
        self.client.force_login(self.test_user)

    def test_post_deletes_event(self):
        event = Event.objects.create(title='Topple Regime', description='they goin down', date=date.today())
        data = {
            'delete_event': [''],
            'event_id': event.pk,
        }
        response = self.client.post(reverse('month_page', kwargs={'month':2, 'year': 2022}), data)
        self.assertEqual(len(Event.objects.all()), 0)
