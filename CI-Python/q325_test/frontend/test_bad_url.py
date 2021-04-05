from seleniumbase import BaseCase

from q325_test.conftest import base_url


class FrontEndBadPageTest(BaseCase):

    def test_bad_url_404(self, *_):
        """
        R8.1.1: Test that user receives error page after accessing unavailable page
        """
        self.open(base_url + '/nonexistent-page')
        self.assertIn('404', self.driver.title)
