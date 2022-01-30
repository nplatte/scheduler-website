from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from django.contrib.auth.models import User

from django.test import LiveServerTestCase
import unittest


class UserMakesEvent(LiveServerTestCase):

    def setUp(self):
        # Tiddlywinks is a super cool person who decided to use the Scheduling app to get their life in order
        # first they boot up Firefox
        self.browser = webdriver.Firefox()
        self.test_username = 'tiddlywinks'
        self.test_password = 'Sparta12456'
        
        # Then Tiddlywinks types in the url
        self.browser.get('http://localhost:8000')

    def tearDown(self):
        # Finally Tiddlywinks logs off the website
        self.browser.quit()

    def _get_username_and_password_inputs(self):
        username = self.browser.find_element_by_id('username')
        password = self.browser.find_element_by_id('password')
        submit = self.browser.find_element_by_id('login_button')
        return username, password, submit

    def test_tiddlywinks_can_make_event(self):
        # Tiddlywinks is greeted by a log in screen
        self.assertIn('Log In', self.browser.title)
        # They enter their username and password
        username_input, password_input, login_button = self._get_username_and_password_inputs()
        username_input.send_keys(self.test_username)
        password_input.send_keys('assword123')
        login_button.click()
        # Oh no! They entered it wrong and got prompted to reenter the information
        self.assertNotIn('Scheduler', self.browser.title)
        # There we go, they enter the password right and can see the month view of the current month
        username_input, password_input, login_button = self._get_username_and_password_inputs()
        username_input.send_keys(self.test_username)
        password_input.send_keys(self.test_password)
        login_button.click()
        self.assertIn('Scheduler', self.browser.title)
        # They click on the first day of the month and a form pops up
        day_one = self.browser.find_element_by_class_name('day_1')
        with self.assertRaises(NoSuchElementException):
            name_input = self.browser.find_element_by_class_name('event_name')
        day_one.click()
        name_input = self.browser.find_element_by_class_name('event_name')
        color_input = self.browser.find_element_by_class_name('event_color')
        time_input = self.browser.find_element_by_class_name('event_time')
        # they enter in the basic information and save the info
        name_input.send_keys('topple regime')
        # the form populates the month day with a color showing an event for that day
        event = self.browser.find_element_by_class_name('topple regime')
        
        


if __name__ == '__main__':
    unittest.main()