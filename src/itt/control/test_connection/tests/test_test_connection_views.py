from django.test import TransactionTestCase
from django.test.client import Client

from test_connection.models import TestConnection


class TestTestConnectionViews(TransactionTestCase):

    fixtures = ['test_test_connection']

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

    def test_post_update_ok_values(self):
        """POST to the TestConnection update.html (Update Test Connection).
        """ 
        # Check that the "host" field is "localhost" before the update.
        tc_before_upd = TestConnection.objects.get(name='conn from fixture')

        # Host.
        expected = "localhost"
        msg = 'TestConnection "host" before update should be "False"'
        self.assertEqual(tc_before_upd.host, expected, msg)

        request_post = {u'name': [u'conn from fixture'],
                        u'host': [u'banana'],
                        u'port': [u'1234'],
                        u'protocol': [u'tftp'],
                        u'submit': [u'Update Test Connection'], }

        response = self._c.post('/testconnection/', request_post)
        msg = 'TestConnection index.html POST status_code not 302 (Redirect)'
        self.assertEqual(response.status_code, 302, msg)

        # Check the database directly.
        tc = TestConnection.objects.get(name='conn from fixture')

        # Host.
        expected = "banana"
        msg = 'TestConnection "host" after update should be "%s"' % expected
        self.assertEqual(tc.host, expected, msg)

    def test_post_delete_test_config(self):
        """Test a POST to the TestContent index.html (Delete Test Content).
        """
        # First, insert a record into the database.
        request_post = {u'name': [u'test connection del'],
                        u'host': [u'localhost'],
                        u'port': [u'1234'],
                        u'protocol': [u'http'],
                        u'submit': [u'Add Test Connection'], }
        response = self._c.post('/testconnection/', request_post)
        msg = 'TestConnection POST to server status_code not 302 (Redirect)'
        self.assertEqual(response.status_code, 302, msg)

        # Query the DB directly to ensure that it exists.
        instance = TestConnection.objects.get(name='test connection del')

        # Now delete it.
        request_post = {u'submit': [u'test_connection_del_pk_%d' %
                                    instance.pk]}
        response = self._c.post('/testconnection/delete/', request_post)
        msg = 'TestConnection POST to delete status_code not 304 (Redirect)'
        self.assertEqual(response.status_code, 302, msg)

        # Finally, check the database.
        with self.assertRaises(TestConnection.DoesNotExist):
            TestConnection.objects.get(name='test connection del')

    @classmethod
    def tearDownClass(cls):
        cls._cls = None
