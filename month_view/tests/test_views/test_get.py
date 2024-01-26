from django.test import LiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User

import month_view.forms as forms



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


class TestViewGETContext(LiveServerTestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='test_user', password='password')
        self.client.force_login(self.test_user)
        view_data = {'month': 2, 'year': 2022}
        self.response = self.client.get(reverse('month_page', kwargs=view_data), follow=True)

    def test_get_context_new_event_form(self):
        self.assertIsInstance(self.response.context['new_form'], forms.NewEventForm)

    def test_get_context_edit_event_form(self):
        self.assertIsInstance(self.response.context['edit_form'], forms.EditEventForm)

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