from selenium import webdriver
import unittest


class UserMakesEvent(unittest.TestCase):

    def setUp(self):
        # Tiddlywinks is a super cool person who decided to use the Scheduling app to get their life in order
        # first they boot up Firefox
        self.browser = webdriver.Firefox()
        
        # Then Tiddlywinks types in the url
        self.browser.get('http://localhost:8000')

    def tearDown(self):
        # Finally Tiddlywinks logs off the website
        self.browser.quit()

    def test_user_can_make_event(self):
        pass


if __name__ == '__main__':
    unittest.main()