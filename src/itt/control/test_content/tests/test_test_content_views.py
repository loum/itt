from django.test import TransactionTestCase
from django.test.client import Client

from test_content.models import TestContent


class TestTestContentViews(TransactionTestCase):

    fixtures = ['test_test_content']

    @classmethod
    def setUpClass(cls):
        cls._c = Client()

    def test_get(self):
        """Test a GET request to the TestContent index.html.
        """
        response = self._c.get('/testcontent/')

        msg = 'TestContent index.html GET status_code not 200 (OK)'
        self.assertEqual(response.status_code, 200, msg)

    def test_post_no_values(self):
        """Post an empty request to the TestContent index.html.
        """
        request_post = {u'submit': ['Add Test Content'], }
        with self.assertRaises(ValueError):
            self._c.post('/testcontent/', request_post)

    def test_post_insert_ok_values(self):
        """POST to the TestContent index.htm (Add Content).
        """
        request_post = {u'name': [u'tester'],
                        u'static': [u'off'],
                        u'bytes': [u'0'],
                        u'submit': [u'Add Content'], }
        response = self._c.post('/testcontent/', request_post)
        msg = 'TestContent index.html POST status_code not 302 (Redirect)'
        self.assertEqual(response.status_code, 302, msg)

        # Check the database directly.
        tc = TestContent.objects.get(name='tester')

        # Static.
        msg = '"TestConfig.static" after insert should be "False"'
        self.assertTrue(tc.static, msg)

        # Bytes.
        expected = 0
        msg = '"TestConfig.bytes" after insert should be %s' % expected
        self.assertEqual(tc.bytes, expected, msg)

    def test_post_update_ok_values(self):
        """POST to the TestContent update.html (Update Test Config).
        """
        # Check that the "bytest" field equals 1024 before the update.
        tc_before_update = TestContent.objects.get(name='test from fixture')

        # Bytes.
        expected = 1024
        msg = '"TestContent.bytes" before update should be 1024'
        self.assertEqual(tc_before_update.bytes, expected, msg)

        # Prepare the update data.
        request_post = {u'name': [u'test from fixture'],
                        u'static': [u'on'],
                        u'bytes': [u'2048'],
                        u'submit': [u'Update Test Content'], }

        response = self._c.post('/testconfig/', request_post)
        msg = 'TestConfig index.html POST status_code not 302 (Redirect)'
        self.assertEqual(response.status_code, 302, msg)

        # Check the database directly.
        tc = TestContent.objects.get(name='test from fixture')

        # Static.
        msg = '"TestContent.static" after update should be True'
        self.assertTrue(tc.static, msg)

        # Bytes.
        expected = 2048
        msg = '"TestContent.bytes" after update should be 2048'
        self.assertEqual(tc.bytes, expected, msg)

    def test_post_delete_test_config(self):
        """Test a POST to the TestContent index.html (Delete Test Content).
        """
        # First, insert a record into the database.
        request_post = {u'name': [u'test content delete'],
                        u'static': [u'off'],
                        u'bytes': [u'1024'],
                        u'submit': [u'Add Test Content'], }
        response = self._c.post('/testcontent/', request_post)
        msg = 'TestContent POST to server status_code not 302 (Redirect)'
        self.assertEqual(response.status_code, 302, msg)

        # Query the DB directy to ensure that it exists.
        instance = TestContent.objects.get(name='test content delete')

        # Now delete it.
        request_post = {u'submit': [u'test_content_del_pk_%d' %
                                    instance.pk]}
        response = self._c.post('/testcontent/delete/', request_post)
        msg = 'TestContent POST to delete status_code not 302 (Redirect)'
        self.assertEqual(response.status_code, 302, msg)

        # Finally, check the database.
        with self.assertRaises(TestContent.DoesNotExist):
            TestContent.objects.get(name='test content delete')

    @classmethod
    def tearDownClass(cls):
        cls._c = None
