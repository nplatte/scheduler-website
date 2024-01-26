from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


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

    def test_decemeber_goes_to_january(self):
        response = self.client.post(reverse('month_page', kwargs={'month': 12, 'year': 2022}), self.data, follow=True)
        self.assertEqual(2023, response.context['year_number'])

    def test_gets_events_for_current_month(self):
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