from django.test import TransactionTestCase
from django.test.client import Client


class TestTestCaseViews(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls._c = Client()

    def test_get(self):
        """GET request to the TestCase index.html.
        """
        r = self._c.get('/testcase/')
        msg = 'TestCase index.html GET status_code not 200 (OK)'
        self.assertEqual(r.status_code, 200, msg)

    @classmethod
    def tearDownClass(cls):
        cls._c = None
