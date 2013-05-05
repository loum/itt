from django.test import TransactionTestCase
from django.test.client import Client

class TestTestConfigViews(TransactionTestCase):

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
        request_post = {u'submit' : ['Add Test Configuration'],}
        with self.assertRaises(ValueError):
            self._c.post('/testconfig/', request_post)

    @classmethod
    def tearDownClass(cls):
        cls._c = None
