from django.test import TransactionTestCase
from django.test.client import Client


class TestTestCheckpointViews(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls._c = Client()

    def test_get(self):
        """GET request to the TestCheckpoint index.html.
        """
        response = self._c.get('/testcheckpoint/')

        msg = 'TestCheckpoint index.html GET status_code not 200 (OK)'
        self.assertEqual(response.status_code, 200, msg)

    @classmethod
    def tearDownClass(cls):
        cls._c = None
