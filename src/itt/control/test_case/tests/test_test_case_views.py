from django.test import TransactionTestCase
from django.test.client import Client

from test_case.models import TestCase
from test_config.models import TestConfig
from test_content.models import TestContent
from test_connection.models import TestConnection


class TestTestCaseViews(TransactionTestCase):

    fixtures = ['test_test_config',
                'test_test_content',
                'test_test_connection']

    @classmethod
    def setUpClass(cls):
        cls._c = Client()

    def test_get(self):
        """GET request to the TestCase index.html.
        """
        r = self._c.get('/testcase/')
        msg = 'TestCase index.html GET status_code not 200 (OK)'
        self.assertEqual(r.status_code, 200, msg)

    def test_post_no_values(self):
        """POST request to the TestCase index.html.
        """
        request_post = {u'submit': ['Add Test Case'], }
        with self.assertRaises(ValueError):
            self._c.post('/testcase/', request_post)

    def test_post_insert_ok_values(self):
        """POST to the TestCase index.html (Add Test Connection).
        """
        request_post = {u'name': [u'tester'],
                        u'test_configuration': [u'1'],
                        u'test_content': [u'1'],
                        u'test_connection': [u'1'],
                        u'submit': [u'Add Test Case'], }
        r = self._c.post('/testcase/', request_post)
        msg = 'TestCase index.html POST status_code not 302 (Redirect)'
        self.assertEqual(r.status_code, 302, msg)

        # Check the database directly.
        tc = TestCase.objects.get(name='tester')

        # Configuration.
        expected = 'config from fixture'
        received = TestConfig.objects.get(pk=tc.test_configuration_id)
        msg = 'Post-insert check should return config name "%s"' % expected
        self.assertEqual(expected, received.name, msg)

        # Content.
        expected = 'content from fixture'
        received = TestContent.objects.get(pk=tc.test_connection_id)
        msg = ('Post-insert check should return connection name "%s"' %
               expected)
        self.assertEqual(expected, received.name, msg)

        # Connection.
        expected = 'conn from fixture'
        received = TestConnection.objects.get(pk=tc.test_content_id)
        msg = 'Post-insert check should return content name "%s"' % expected
        self.assertEqual(expected, received.name, msg)

    @classmethod
    def tearDownClass(cls):
        cls._c = None
