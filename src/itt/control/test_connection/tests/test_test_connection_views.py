from django.test import TransactionTestCase
from django.test.client import Client


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

    @classmethod
    def tearDownClass(cls):
        cls._cls = None
