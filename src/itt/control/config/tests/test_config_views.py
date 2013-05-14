from django.test import TransactionTestCase
from django.test.client import Client

class TestConfigViews(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls._c = Client()

    def test_get(self):
        """Test a GET request to the Config index.html.
        """
        response = self._c.get('/config/')

        msg = 'Config index.html GET status_code not 200 (OK)'
        received = response.status_code
        expected = 200
        self.assertEqual(received, expected, msg)

    def test_post(self):
        """Test a POST request to the Config index.html.
        """
        request_post = {u'standalone': [u'on'],
                        u'submit': [u'Change Settings'],
                        u'server': [u'on'],
                        u'client': [u'on'],
                        u'role': [u'ma'],}

        response = self._c.post('/config/', request_post)

        msg = 'Config index.html POST status_code not 302 (redirection)'
        received = response.status_code
        expected = 302
        self.assertEqual(received, expected, msg)

    def test_post_cancel(self):
        """Test a POST request cancel to the Config index.html.
        """
        request_post = {u'standalone': [u'on'],
                        u'cancel': [u'Cancel'],
                        u'server': [u'on'],
                        u'client': [u'on'],
                        u'role': [u'ma'],}

        response = self._c.post('/config/', request_post)

        msg = 'Config index.html POST status_code not 302 (redirection)'
        received = response.status_code
        expected = 302
        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        cls._c = None
