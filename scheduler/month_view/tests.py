from operator import length_hint
from django.http import response
from django.urls import reverse
from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models import User

import datetime, calendar

import month_view.views as views
import month_view.forms as forms


class TestLoginPage(LiveServerTestCase):

    '''the login page needs to be the first page people see
    it needs to use the right template
    redirect good users to month view
    redirect bad users to login page'''

    def setUp(self):
        self.test_username = 'winkstiddly'
        self.test_password = 'password123'
        User.objects.create_user(username=self.test_username, email='test@test.com', password=self.test_password)

    def tearDown(self):
        pass

    def test_login_uses_right_template(self):
        response = self.client.get(reverse('login_page'))
        self.assertTemplateUsed(response,'month_view/login.html')

    def test_login_redirects_to_month_view_on_success(self):
        response = self.client.post(reverse('login_page'), {'username': self.test_username, 'password': self.test_password}, follow=True)
        self.assertRedirects(response, 'month_view/')

    def test_login_redirects_to_login_on_fail(self):
        response = self.client.post(reverse('login_page'), {'username': self.test_username, 'password': 'wrong_password'}, follow=True)
        self.assertRedirects(response, reverse('login_page'))

    def test_login_required_redirects_to_login_page(self):
        response = self.client.get(reverse('month_page'), follow=True)
        self.assertTemplateUsed(response, 'month_view/login.html')


class TestMonthViewPage(LiveServerTestCase):

    '''
    Month View Tests:
    -User cannot view without logging in
    '''

    def setUp(self):
        pass

    def test_month_view_requires_login(self):
        response = self.client.get(reverse('month_page'), follow=True)
        self.assertTemplateNotUsed(response, 'month_view/month_view.html')


class TestHelperFunctions(TestCase):

    def setUp(self):
        self.month = datetime.datetime.now().month

    def test_get_month_days(self):
        self.assertEqual(len(views._get_days_in_month(1, 2022)), 31)


class TestNewEventForm(TestCase):

    def test_inputs_have_class_names(self):
        new_event_form = forms.EventForm()
        self.assertIn('class="event_name"', new_event_form.as_p())
        self.assertIn('class="event_color"', new_event_form.as_p())
        self.assertIn('class="event_time"', new_event_form.as_p())
