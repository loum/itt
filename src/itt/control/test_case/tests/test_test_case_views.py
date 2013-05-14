from django.test import TransactionTestCase
from django.test.client import Client

from test_case.models import TestCase
from test_config.models import TestConfig
from test_content.models import TestContent
from test_connection.models import TestConnection


class TestTestCaseViews(TransactionTestCase):

    fixtures = ['test_test_config',
                'test_test_content',
                'test_test_connection',
                'test_test_case']

    @classmethod
    def setUpClass(cls):
        cls._c = Client()
        cls._test_name = 'case from fixture'

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

    def test_post_update_ok_values(self):
        """POST to the TestCase update.html (Update Test Case).
        """
        # Check that name of the test config before the update.
        tc_before_upd = TestCase.objects.get(name='%s' % self._test_name)

        # Test Config name.
        id = tc_before_upd.test_configuration_id
        expected = 'config from fixture'
        received = TestConfig.objects.get(pk=id)
        msg = 'Existing check should return config name "%s"' % expected
        self.assertEqual(expected, received.name, msg)

        # Prepare the update request POST.
        request_post = {u'name': [u'%s' % self._test_name],
                        u'test_configuration': [u'2'],
                        u'test_content': [u'1'],
                        u'test_connection': [u'1'],
                        u'submit': [u'Update Test Case'], }

        response = self._c.post('/testcase/', request_post)
        msg = 'TestCase index.html POST status_code not 302 (Redirect)'
        self.assertEqual(response.status_code, 302, msg)

        # Check that name of the test config after the update.
        tc_after_upd = TestCase.objects.get(name='%s' % self._test_name)

        # Test Config name.
        id = tc_after_upd.test_configuration_id
        expected = 'config2 from fixture'
        received = TestConfig.objects.get(pk=id)
        msg = 'Existing check should return config name "%s"' % expected
        self.assertEqual(expected, received.name, msg)


    def test_post_delete_test_case(self):
        """POST delete request to the TestCase index.html (Delete Test Case).
        """
        # Query the DB directly to ensure that it exists.
        instance = TestCase.objects.get(name='%s' % self._test_name)

        # Now delete it.
        request_post = {u'submit': [u'test_case_del_pk_%d' %
                                    instance.pk]}
        response = self._c.post('/testconnection/delete/', request_post)
        msg = 'TestCase POST to delete status_code not 302 (Redirect)'
        self.assertEqual(response.status_code, 302, msg)

        # Finally, check the database.
        with self.assertRaises(TestCase.DoesNotExist):
            TestCase.objects.get(name='%s' % self._test_name)

    @classmethod
    def tearDownClass(cls):
        cls._c = None
        cls._test_name = None
