from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains

from django.contrib.auth.models import User
from month_view.models import Event
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from datetime import datetime
from django.test import TestCase
from time import sleep


NEW_EVENT_CLASS_IDS = {
    'title_class': 'event_title_input',
    'title_id': 'new_event_title',
    'time_class': 'event_time_input',
    'time_id': 'new_event_time',
    'date_class': 'event_date_input',
    'date_id': 'new_event_date',
    'description_class': 'event_description_input',
    'description_id': 'new_event_description',
    'submit_button': 'new_event_submit_button',
}

EDIT_EVENT_CLASS_IDS = {
    'title_class': 'event_title_input',
    'title_id': 'edit_event_title',
    'time_class': 'event_time_input',
    'date_class': 'event_date_input',
    'date_id': 'edit_event_date',
    'description_class': 'event_description_input',
    'description_id': 'edit_event_description',
    'submit_button': 'edit_event_submit_button'
}


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

    def _make_new_event(self, name, day):
        day_div = self.browser.find_element_by_class_name(f'day_{day}')
        action = ActionChains(self.browser)
        action.move_to_element(day_div).perform()
        new_event_button = self.browser.find_element_by_id(f'new_event_button_{day}')
        new_event_button.click()
        name_input = self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['title_id'])
        submit_button = self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['submit_button'])
        name_input.send_keys(name)
        submit_button.click()

    def _make_new_event_last_month(self, name, day):
        day_div = self.browser.find_element_by_class_name(f'last_month_day_{day}')
        action = ActionChains(self.browser)
        action.move_to_element(day_div).perform()
        new_event_button = self.browser.find_element_by_id(f'last_month_new_event_button_{day}')
        new_event_button.click()
        name_input = self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['title_id'])
        submit_button = self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['submit_button'])
        name_input.send_keys(name)
        submit_button.click()

    def _make_new_event_next_month(self, name, day):
        day_div = self.browser.find_element_by_class_name(f'next_month_day_{day}')
        action = ActionChains(self.browser)
        action.move_to_element(day_div).perform()
        new_event_button = self.browser.find_element_by_id(f'next_month_new_event_button_{day}')
        new_event_button.click()
        name_input = self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['title_id'])
        submit_button = self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['submit_button'])
        name_input.send_keys(name)
        submit_button.click()

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
        action = ActionChains(self.browser)
        # Tiddlywinks logs in to  the website
        self._login_attempt(self.test_username, self.test_password)
        # They click on the first day of the month and a form pops up
        day_one = self.browser.find_element_by_class_name('day_1')
        bad_name_input = self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['title_id'])
        self.assertRaises(ElementNotInteractableException, bad_name_input.send_keys, 'something')
        action.move_to_element(day_one).perform()
        new_event_button = self.browser.find_element_by_id(f'new_event_button_1')
        new_event_button.click()
        name_input = self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['title_id'])
        self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['time_id'])
        self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['date_id'])
        submit_button = self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['submit_button'])
        # they enter in the basic information and save the info
        name_input.send_keys('topple regime')
        submit_button.click()
        # the form populates the month day with a color showing an event for that day
        events = self.browser.find_elements_by_class_name('day_1_event')
        self.assertEqual(len(events), 1)
        # happy with her new event, she logs off
        self._logout_attempt()

    def test_tiddlywinks_can_edit_event(self):
        # Tiddlywinks logs in to  the website
        self._login_attempt(self.test_username, self.test_password)
        # she makes an event badly
        self._make_new_event('defeat shoes', 1)
        # she decides to correct it
        # she clicks on the event
        event = self.browser.find_element_by_class_name('day_1_event')
        event.click()
        # she sees a new form pop up with her old data
        edit_title_input = self.browser.find_element_by_id(EDIT_EVENT_CLASS_IDS['title_id'])
        self.assertEqual('defeat shoes', edit_title_input.get_attribute('value'))
        # she puts her new title in and clicks submit
        edit_title_input.clear()
        edit_title_input.send_keys('de-feet shoes')
        submit_button = self.browser.find_element_by_id(EDIT_EVENT_CLASS_IDS['submit_button'])
        submit_button.click()
        # she sees her updated event on the same day
        event = self.browser.find_element_by_class_name('day_1_event')
        event.click()
        edit_title_input = self.browser.find_element_by_id(EDIT_EVENT_CLASS_IDS['title_id'])
        self.assertEqual('de-feet shoes', edit_title_input.get_attribute('value'))
        self.assertEqual(1, len(Event.objects.all()))
        # she logs out
        self._logout_attempt()

    def test_tiddlywinks_can_delete_an_event(self):
        # Tiddlywinks logs in to  the website
        self._login_attempt(self.test_username, self.test_password)
        # she makes a bad event
        self._make_new_event('this event sucks', 1)
        # she decides to delete that event
        # she clicks on her event and clicks the delete button
        event = self.browser.find_element_by_class_name('day_1_event')
        event.click()
        delete_button = self.browser.find_element_by_id('delete_button')
        delete_button.click()
        # the form dissappears
        bad_name_input = self.browser.find_element_by_id(EDIT_EVENT_CLASS_IDS['title_id'])
        self.assertRaises(ElementNotInteractableException, bad_name_input.send_keys, 'something')
        # she doesn't see her event anymore
        events_on_1 = self.browser.find_elements_by_class_name('day_1_event')
        self.assertEqual(0, len(events_on_1))
        self.assertEqual(0, len(Event.objects.all()))
        # she logs out
        self._logout_attempt()

    def test_tiddlywinks_can_cancel_changes_or_new_event(self):
        # Tiddlywinks logs in to  the website
        self._login_attempt(self.test_username, self.test_password)
        # she makes an event on the 5th day of the month
        self._make_new_event('brothday party', 5)
        # she clicks on the event to edit it
        event = self.browser.find_element_by_class_name('day_5_event')
        event.click()
        # she don't wanna edit it so she clicks cancel
        cancel_button = self.browser.find_element_by_id('edit_cancel_button')
        cancel_button.click()
        # the form dissappears
        bad_name_input = self.browser.find_element_by_id(EDIT_EVENT_CLASS_IDS['title_id'])
        self.assertRaises(ElementNotInteractableException, bad_name_input.send_keys, 'something')
        # she decides to make a new event
        day_div = self.browser.find_element_by_class_name(f'day_4')
        action = ActionChains(self.browser)
        action.move_to_element(day_div).perform()
        new_event_button = self.browser.find_element_by_id(f'new_event_button_4')
        new_event_button.click()
        self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['title_id'])
        # she gives up because life is hard and decides to cancel the event
        cancel_button = self.browser.find_element_by_id('new_cancel_button')
        cancel_button.click()
        bad_name_input = self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['title_id'])
        self.assertRaises(ElementNotInteractableException, bad_name_input.send_keys, 'something')
        # she logs out
        self._logout_attempt()

    def test_tiddlywinks_can_make_plan_for_month_out(self):
        # Tiddlywinks logs in to  the website
        self._login_attempt(self.test_username, self.test_password)
        # after making her first event, she decides to make a new event in the next month
        # shee sees the current month on the top of the page
        month_name = self.browser.find_element_by_id('month_name')
        self.assertEqual(month_name.text, _get_month_name(datetime.now().month))
        # she clicks the arrow button and sees she isn't on the current month
        right_arrow = self.browser.find_element_by_id('right_month')
        right_arrow.click()
        month_name = self.browser.find_element_by_id('month_name')
        self.assertEqual(month_name.text, _get_month_name(datetime.now().month + 1))
        # she clicks the 5th and makes a new event for that day
        self._make_new_event('topple regime', 5)
        # she sees her event on the calender
        events_on_the_fifth = self.browser.find_elements_by_class_name('day_5_event')
        self.assertEqual(1, len(events_on_the_fifth))
        # happy with her new event, she logs off
        self._logout_attempt()

    def test_tiddlywinks_can_make_event_for_last_year(self):
        # Tiddlywinks logs in to  the website
        self._login_attempt(self.test_username, self.test_password)
        # she sees that the current month and year are on the screen
        month_name = self.browser.find_element_by_id('month_name')
        year_num = self.browser.find_element_by_id('year_number')
        self.assertEqual(month_name.text, _get_month_name(datetime.now().month))
        self.assertEqual('2022', year_num.text)
        # she decides she wants to edit an event from last year, because she is a lil shit
        # she clicks the left arrow button and sees the month swap to the previous month
        left_arrow = self.browser.find_element_by_id('left_month')
        left_arrow.click()
        month_name = self.browser.find_element_by_id('month_name')
        self.assertEqual(month_name.text, _get_month_name(datetime.now().month - 1))
        # she clicks 11 more times to make sure she is in the last year
        for i in range(11):
            left_arrow = self.browser.find_element_by_id('left_month')
            left_arrow.click()
        # she sees she is in the last year
        year_num = self.browser.find_element_by_id('year_number')
        self.assertEqual('2021', year_num.text)
        # she makes the event
        self._make_new_event('Twinks necromancy', 1)
        # the form dissappears when she presses submit
        bad_name_input = self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['title_id'])
        self.assertRaises(ElementNotInteractableException, bad_name_input.send_keys, 'something')
        # she arrows right for a full year until she's back in the current month
        for i in range(12):
            right_arrow = self.browser.find_element_by_id('right_month')
            right_arrow.click()
        # she logs out
        self._logout_attempt()

    def test_tiddlywinks_can_make_event_on_greyed_out_next_month_days(self):
        # she logs in
        self._login_attempt(self.test_username, self.test_password)
        # she wants to make an event for next month
        # she clicks on the plus sign on the first day and makes an event
        day_div = self.browser.find_element_by_class_name(f'next_month_day_1')
        action = ActionChains(self.browser)
        action.move_to_element(day_div).perform()
        new_event_button = self.browser.find_element_by_id(f'next_month_new_event_button_1')
        new_event_button.click()
        # She sees the date is for next month
        date_input = self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['date_id'])
        self.assertEqual('2022-7-1', date_input.get_attribute('value'))
        # she puts in her event info
        name_input = self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['title_id'])
        submit_button = self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['submit_button'])
        name_input.send_keys('destory world')
        submit_button.click()
        # she sees her event on screen
        events = self.browser.find_elements_by_class_name('next_day_1_event')
        self.assertEqual(len(events), 1)
        # She makes sure the event got added to the right day
        event = self.browser.find_element_by_class_name('next_day_1_event')
        event.click()
        # she realizes she needs to change the event
        edit_title_input = self.browser.find_element_by_id(EDIT_EVENT_CLASS_IDS['title_id'])
        edit_title_input.clear()
        edit_title_input.send_keys('de-feet shoes')
        submit_button = self.browser.find_element_by_id(EDIT_EVENT_CLASS_IDS['submit_button'])
        submit_button.click()
        # she sees her updated event on the same day
        event = self.browser.find_element_by_class_name('next_day_1_event')
        event.click()
        edit_title_input = self.browser.find_element_by_id(EDIT_EVENT_CLASS_IDS['title_id'])
        self.assertEqual('de-feet shoes', edit_title_input.get_attribute('value'))
        self.assertEqual(1, len(Event.objects.all()))
        # she then logs off
        self._logout_attempt()

    def test_tiddlywinks_can_make_and_edit_event_on_greyed_out_last_month_days(self):
        # she logs in
        self._login_attempt(self.test_username, self.test_password)
        # she wants to make an event for next month
        # she clicks on the plus sign on the first day and makes an event
        day_div = self.browser.find_element_by_class_name(f'last_month_day_31')
        action = ActionChains(self.browser)
        action.move_to_element(day_div).perform()
        new_event_button = self.browser.find_element_by_id(f'last_month_new_event_button_31')
        new_event_button.click()
        # She sees the date is for next month
        date_input = self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['date_id'])
        self.assertEqual('2022-5-31', date_input.get_attribute('value'))
        # she puts in her event info
        name_input = self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['title_id'])
        submit_button = self.browser.find_element_by_id(NEW_EVENT_CLASS_IDS['submit_button'])
        name_input.send_keys('destory world')
        submit_button.click()
        # she sees her event on screen
        events = self.browser.find_elements_by_class_name('last_day_31_event')
        self.assertEqual(len(events), 1)
        # She makes sure the event got added to the right day
        event = self.browser.find_element_by_class_name('last_day_31_event')
        event.click()
        # she realizes she needs to change the event
        edit_title_input = self.browser.find_element_by_id(EDIT_EVENT_CLASS_IDS['title_id'])
        edit_title_input.clear()
        edit_title_input.send_keys('de-feet shoes')
        submit_button = self.browser.find_element_by_id(EDIT_EVENT_CLASS_IDS['submit_button'])
        submit_button.click()
        # she sees her updated event on the same day
        event = self.browser.find_element_by_class_name('last_day_31_event')
        event.click()
        edit_title_input = self.browser.find_element_by_id(EDIT_EVENT_CLASS_IDS['title_id'])
        self.assertEqual('de-feet shoes', edit_title_input.get_attribute('value'))
        self.assertEqual(1, len(Event.objects.all()))
        # she then logs off
        self._logout_attempt()

    def test_tiddly_winks_can_make_and_edit_event_around_year_end(self):
        # Tiddlywinks logs in
        self._login_attempt(self.test_username, self.test_password)
        # she goes to January and decides to make an event on the 31st of December
        for i in range(datetime.now().month - 1):
            left_arrow = self.browser.find_element_by_id('left_month')
            left_arrow.click()
        month_name = self.browser.find_element_by_id('month_name')
        self.assertEqual('January', month_name.text)
        # she tries to make an event on December 31
        self._make_new_event_last_month('destroy world calendars', 31)
        # she sees her event on the 31st and goes over to december to view it proper
        left_arrow = self.browser.find_element_by_id('left_month')
        left_arrow.click()
        event = self.browser.find_element_by_class_name('day_31_event')
        event.click()
        edit_title_input = self.browser.find_element_by_id(EDIT_EVENT_CLASS_IDS['title_id'])
        self.assertEqual('destroy world calend', edit_title_input.get_attribute('value'))
        # she then tries to make a new years day event
        self._make_new_event_next_month('party', 1)
        # she sees her event on January 1
        event = self.browser.find_element_by_class_name('next_day_1_event')
        event.click()
        edit_title_input = self.browser.find_element_by_id(EDIT_EVENT_CLASS_IDS['title_id'])
        self.assertEqual('party', edit_title_input.get_attribute('value'))
        # she logs out and takes a nap
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
        self.assertEqual(test_month, 'June')
