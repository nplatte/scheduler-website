from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class UserMakesEvent(unittest.TestCase):

    def setUp(self):
        # Tiddlywinks is a super cool person who decided to use the Scheduling app to get their life in order
        # first they boot up Firefox
        self.browser = webdriver.Firefox()
        self.test_username = 'tiddlywinks'
        self.test_password = 'password123'
        
        # Then Tiddlywinks types in the url
        self.browser.get('http://localhost:8000')

    def tearDown(self):
        # Finally Tiddlywinks logs off the website
        self.browser.quit()

    def test_tiddlywinks_can_make_event(self):
        # Tiddlywinks is greeted by a log in screen
        self.assertIn('Log In', self.browser.title)
        # They enter their username and password
        username_input = self.browser.find_element_by_id('username')
        password_input = self.browser.find_element_by_id('password')
        username_input.send_keys(self.test_username)
        password_input.send_keys('assword123')
        password_input.send_keys(Keys.ENTER)
        # Oh no! They entered it wrong and got prompted to reenter the information
        self.assertNotIn('Scheduler', self.browser.title)
        # There we go, they enter the password right and can see the month view of the current month
        username_input.send_keys(self.test_username)
        password_input.send_keys(self.test_password)
        password_input.send_keys(Keys.ENTER)
        self.assertIn('Scheduler', self.browser.title)
        # They click on the first day of the month and a form pops up
        # they enter in the basic information and save the info
        # the form populates the month day with a color showing an event for that day
        pass
        


if __name__ == '__main__':
    unittest.main()