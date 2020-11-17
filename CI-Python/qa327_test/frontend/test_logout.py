from seleniumbase import BaseCase

from qa327_test.conftest import base_url


class FrontEndLogoutTest(BaseCase):

    def test_logout_redirect(self, *_):
        """
        R7.1.1: Test that user is redirected to /login after logout
        """
        self.open(base_url + '/logout')
        self.assertEqual(self.driver.current_url, base_url + '/login')

    def test_logout_login(self, *_):
        """
        R7.1.2: Test that user can access /login after logout
        """
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        self.assertEqual(self.driver.current_url, base_url + '/login')

    def test_logout_register(self, *_):
        """
        R7.1.3: Test that user can access /register after logout
        """
        self.open(base_url + '/logout')
        self.open(base_url + '/register')
        self.assertEqual(self.driver.current_url, base_url + '/register')

    def test_logout_homepage_denial(self, *_):
        """
        R7.1.5: Test that user cannot access / after logout
        """
        self.open(base_url + '/logout')
        self.open(base_url + '/')
        self.assertEqual(self.driver.current_url, base_url + '/login')
