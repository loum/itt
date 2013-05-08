from django.test import TransactionTestCase
from django.test.client import Client

from test_content.models import TestContent


class TestTestContentViews(TransactionTestCase):

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
        request_post = {u'submit': ['Add Content'], }
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

    @classmethod
    def tearDownClass(cls):
        cls._c = None
