from django.test import TransactionTestCase
from django.test.client import Client

from test_connection.models import TestConnection


class TestTestConnectionViews(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
       cls._c = Client()

    def test_get(self):
        """Test a GET request to the TestConnection index.html.
        """
        response = self._c.get('/testconnection/')

        msg = 'TestConnection index.html GET status_code not 200 (OK)'
        self.assertEqual(response.status_code, 200, msg)

    def test_post_no_values(self):
        """POST request to the TestConnection index.html.
        """
        request_post = {u'submit': ['Add Test Connection'], }
        with self.assertRaises(ValueError):
            self._c.post('/testconnection/', request_post)

    def test_post_insert_ok_values(self):
        """POST to the TestConnection index.html (Add Test Connection).
        """
        request_post = {u'name': [u'tester'],
                        u'host': [u'localhost'],
                        u'port': [u'1234'],
                        u'protocol': [u'tftp'],
                        u'submit': [u'Add Test Connection'], }
        response = self._c.post('/testconnection/', request_post)
        msg = 'TestConnection index.html POST status_code not 302 (Redirect)'
        self.assertEqual(response.status_code, 302, msg)

        # Check the database directly.
        tc = TestConnection.objects.get(name='tester')

        # Host.
        expected = "localhost"
        msg = '"TestConnection.host" after insert should be "%s" % expected'
        self.assertEqual(tc.host, expected, msg)

        # Port.
        expected = 1234
        msg = '"TestConnection.port" after insert should be "%d" % expected'
        self.assertEqual(tc.port, expected, msg)

        # Protocol.
        expected = "tftp"
        msg = ('"TestConnection.protocol" after insert should be "%s"' %
               expected)
        self.assertEqual(tc.protocol, expected, msg)

    @classmethod
    def tearDownClass(cls):
        cls._cls = None
