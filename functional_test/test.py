from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException


from django.contrib.auth.models import User
from month_view.models import Event

from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time


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
        logout_button = self.browser.find_element_by_id('logout_button')
        logout_button.click()
        # This takes her to the log in page
        self.assertIn('Log In', self.browser.title)

    def test_tiddlywinks_can_make_event(self):
        # Tiddlywinks is greeted by a log in screen
        self.assertIn('Log In', self.browser.title)
        # They enter the right username and password and can see the month view of the current month
        self._login_attempt(self.test_username, self.test_password)
        self.assertIn('Scheduler', self.browser.title)
        # They click on the first day of the month and a form pops up
        day_one = self.browser.find_element_by_class_name('day_1')
        bad_name_input = self.browser.find_element_by_class_name('event_name')
        self.assertRaises(ElementNotInteractableException, bad_name_input.send_keys, 'something')
        day_one.click()
        name_input = self.browser.find_element_by_class_name('event_name')
        description_input = self.browser.find_element_by_class_name('event_description')
        time_input = self.browser.find_element_by_class_name('event_time')
        submit_button = self.browser.find_element_by_id('new_event_submit_button')
        # they enter in the basic information and save the info
        name_input.send_keys('topple regime')
        submit_button.click()
        # the form populates the month day with a color showing an event for that day
        events = self.browser.find_elements_by_class_name('event')
        self.assertEqual(len(events), 1)
