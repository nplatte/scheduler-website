from django.test import TestCase
import month_view.views as views

class TestLoginPage(TestCase):
    # the login page needs to be the first page people see
    # it needs to use the right template
    # redirect good users to month view
    # redirect bad users to login page

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_login_uses_right_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,'month_view/login.html')

    def test_login_redirects_to_month_view_on_success(self):
        pass

    def test_login_redirects_to_login_on_fail(self):
        pass