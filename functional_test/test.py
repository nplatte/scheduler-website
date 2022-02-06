from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from datetime import datetime
from django.test import TestCase
from time import sleep


class UserMakesEvent(StaticLiveServerTestCase):

    def setUp(self):
        # Tiddlywinks is a super cool person who decided to use the Scheduling app to get their life in order
        # first they boot up Firefox
        self.test_username = 'tiddlywinks'
        self.test_password = 'Sparta12456'
        User.objects.create_user(self.test_username, 'test@test.com', self.test_password)
        self.browser = webdriver.Firefox()
        # Then Tiddlywinks types in the url
        self.browser.get(self.live_server_url)

    def tearDown(self):
        # Finally Tiddlywinks logs off the website
        self.browser.quit()

    def _login_attempt(self, username, password):
        username_input = self.browser.find_element_by_id('username')
        password_input = self.browser.find_element_by_id('password')
        login_button = self.browser.find_element_by_id('login_button')
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

    def _logout_attempt(self):
        logout_button = self.browser.find_element_by_id('logout_button')
        logout_button.click()

    def _get_month_name(self, month=datetime.now().month):
        months = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        }
        return months[month]
        
    def test_tiddlywinks_can_log_in_and_out(self):
        # Tiddlywinks is greeted by a log in screen
        self.assertIn('Log In', self.browser.title)
        # They enter their username and password
        self._login_attempt(self.test_username, 'assword123')
        # Oh no! They entered it wrong and got prompted to reenter the information
        self.assertNotIn('Scheduler', self.browser.title)
        self.assertIn('Log In', self.browser.title)
        # There we go, they enter the password right and can see the month view of the current month
        self._login_attempt(self.test_username, self.test_password)
        self.assertIn('Scheduler', self.browser.title)
        # satisfied that her account works, she clicks the logout button
        self._logout_attempt()
        # This takes her to the log in page
        self.assertIn('Log In', self.browser.title)

    def test_tiddlywinks_can_make_event(self):
        # Tiddlywinks logs in to  the website
        self._login_attempt(self.test_username, self.test_password)
        # They click on the first day of the month and a form pops up
        day_one = self.browser.find_element_by_class_name('day_1')
        bad_name_input = self.browser.find_element_by_class_name('new_event_name')
        self.assertRaises(ElementNotInteractableException, bad_name_input.send_keys, 'something')
        day_one.click()
        name_input = self.browser.find_element_by_class_name('new_event_name')
        self.browser.find_element_by_class_name('new_event_description')
        self.browser.find_element_by_class_name('new_event_time')
        submit_button = self.browser.find_element_by_id('new_event_submit_button')
        # they enter in the basic information and save the info
        name_input.send_keys('topple regime')
        submit_button.click()
        # the form populates the month day with a color showing an event for that day
        events = self.browser.find_elements_by_class_name('day_5_event')
        sleep(5)
        self.assertEqual(len(events), 1)
        # happy with her new event, she logs off
        self._logout_attempt()

    def test_tiddlywinks_can_make_plan_for_month_out(self):
        # Tiddlywinks logs in to  the website
        self._login_attempt(self.test_username, self.test_password)
        # after making her first event, she decides to make a new event in the next month
        # she clicks the arrow button and sees she isn't on the current month
        right_arrow = self.browser.find_element_by_id('right_month')
        right_arrow.click()
        month_name = self.browser.find_element_by_class_name('month_name')
        self.assertEqual(month_name, _get_month_name(datetime.now().month + 1))
        # she clicks the 5th and makes a new event for that day
        day_5 = self.browser.find_element_by_class_name('day_5')
        day_5.click()
        # she adds her data for that day and clicks submit
        name_input = self.browser.find_element_by_class_name('event_name')
        submit_button = self.browser.find_element_by_id('new_event_submit_button')
        name_input.send_keys('topple regime')
        submit_button.click()
        # she sees her event on the calender
        events_on_the_fifth = self.browser.find_elements_by_class_name('day_5_event')
        self.assertEqual(1, len(events_on_the_fifth))
        # happy with her new event, she logs off
        self._logout_attempt()

def _get_month_name(month=datetime.now().month):
    months = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }
    return months[month]


class TestHelpers(TestCase):

    def test_get_month_name(self):
        test_month = _get_month_name(datetime.now().month)
        self.assertEqual(test_month, 'February')
