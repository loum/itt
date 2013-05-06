from django.test import TransactionTestCase
from django.test.client import Client

from test_config.models import TestConfig
from test_config.views import _parse_pk


class TestTestConfigViews(TransactionTestCase):

    fixtures = ['test_test_config']

    @classmethod
    def setUpClass(cls):
        cls._c = Client()

    def test_get(self):
        """Test a GET request to the TestConfig index.html.
        """
        response = self._c.get('/testconfig/')

        msg = 'TestConfig index.html GET status_code not 200 (OK)'
        self.assertEqual(response.status_code, 200, msg)

    def test_post_no_values(self):
        """Test a POST request to the TestConfig index.html.
        """
        request_post = {u'submit': ['Add Test Configuration'], }
        with self.assertRaises(ValueError):
            self._c.post('/testconfig/', request_post)

    def test_post_insert_ok_values(self):
        """Test a POST to the TestConfig index.html (Add Test Config).
        """
        request_post = {u'name': [u'tester'],
                        u'upload': [u'on'],
                        u'bytes': [u'1'],
                        u'minimum_gap': [u'2.2'],
                        u'chunk_size': [u'3'],
                        u'submit': [u'Add Test Configuration'], }
        response = self._c.post('/testconfig/', request_post)
        msg = 'TestConfig index.html POST status_code not 302 (Redirect)'
        self.assertEqual(response.status_code, 302, msg)

        # Check the database directly.
        tc = TestConfig.objects.get(name='tester')

        # Upload.
        msg = 'TestConfig "upload" after insert should be "True"'
        self.assertTrue(tc.upload, msg)

        # Bytes.
        expected = 1
        msg = 'TestConfig "bytes" after insert should be %s' % expected
        self.assertEqual(tc.bytes, expected, msg)

        # Minimum gap.
        expected = 2.2
        msg = ('TestConfig "minimum_gap" after insert should be %s' %
               expected)
        self.assertEqual(tc.minimum_gap, expected, msg)

        # Chunk size.
        expected = 3
        msg = ('TestConfig "chunk_size" after insert should be %s' %
               expected)
        self.assertEqual(tc.chunk_size, expected, msg)

    def test_post_update_ok_values(self):
        """Test a POST to the TestConfig update.html (Update Test Config).
        """
        # Check that the "upload" field is False before the update.
        tc_before_update = TestConfig.objects.get(name='test from fixture')

        # Upload.
        msg = 'TestConfig "upload" after update should be "False"'
        self.assertFalse(tc_before_update.upload, msg)

        request_post = {u'name': [u'test from fixture'],
                        u'upload': [u'on'],
                        u'bytes': [u'0'],
                        u'minimum_gap': [u'0.0'],
                        u'chunk_size': [u'0'],
                        u'submit': [u'Update Test Configuration'], }

        response = self._c.post('/testconfig/', request_post)
        msg = 'TestConfig index.html POST status_code not 302 (Redirect)'
        self.assertEqual(response.status_code, 302, msg)

        # Check the database directly.
        tc = TestConfig.objects.get(name='test from fixture')

        # Upload.
        msg = 'TestConfig "upload" after update should be "True"'
        self.assertTrue(tc.upload, msg)

    def test_post_delete_test_config(self):
        """Test a POST to the TestConfig index.html (Delete Test Config).
        """
        # First, insert a record into the database.
        request_post = {u'name': [u'test config delete'],
                        u'upload': [u'off'],
                        u'bytes': [u'0'],
                        u'minimum_gap': [u'0.0'],
                        u'chunk_size': [u'0'],
                        u'submit': [u'Add Test Configuration'], }
        response = self._c.post('/testconfig/', request_post)
        msg = 'TestConfig POST to inserver status_code not 302 (Redirect)'
        self.assertEqual(response.status_code, 302, msg)

        instance = TestConfig.objects.get(name='test config delete')

        # Now delete it.
        request_post = {u'submit': [u'test_config_del_pk_%d' % instance.pk]}

        response = self._c.post('/testconfig/delete/', request_post)
        msg = 'TestConfig POST to delete status_code not 301 (Redirect)'
        self.assertEqual(response.status_code, 302, msg)

        # Finally, check the database.
        with self.assertRaises(TestConfig.DoesNotExist):
            TestConfig.objects.get(name='test config delete')

    def test_parse_pk_valid_edit_input_value(self):
        """Valid parse of a test_config edit input value.
        """
        input_value = 'test_config_edit_pk_2'
        received = _parse_pk(input_value)
        expected = 2
        msg = ('Primary key parse of "%s" did not return %d' %
               (input_value, received))
        self.assertEqual(received, expected, msg)

    def test_parse_pk_invalid_edit_input_value(self):
        """Invalid parse of a test_config edit input value.
        """
        input_value = 'test_config_edit_pk_'
        received = _parse_pk(input_value)
        msg = 'Primary key parse of "%s" did not return None' % input_value
        self.assertIsNone(received, msg)

    @classmethod
    def tearDownClass(cls):
        cls._c = None
