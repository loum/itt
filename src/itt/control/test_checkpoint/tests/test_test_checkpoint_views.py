import json
from django.test import TransactionTestCase
from django.test.client import Client

from test_checkpoint.models import Checkpoint
from itt.utils.files import data_generator


class TestTestCheckpointViews(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls._c = Client()
        cls._mac = '00:11:22:33:44:55'
        cls._checkpoint_uri = '/test/checkpoint/'

    def test_get(self):
        """GET request to the TestCheckpoint index.html.
        """
        response = self._c.get('/testcheckpoint/')

        msg = 'TestCheckpoint index.html GET status_code not 200 (OK)'
        self.assertEqual(response.status_code, 200, msg)

    def test_get_search(self):
        """GET to the TestCheckpoint search.html (Search Test Checkpoints).
        """
        response = self._c.get('/testcheckpoint/search/')

        msg = 'TestCheckpoint search.html GET status_code not 200 (OK)'
        self.assertEqual(response.status_code, 200, msg)

    def test_post_results_no_node(self):
        """POST to the TestCheckpoint results.html with no node defined.
        """
        request_post = {u'submit': [u'Search Test Checkpoints']}
        response = self._c.post('/testcheckpoint/results/', request_post)

        msg = 'TestCheckpoint result.html POST status_code not 302 (Redirect)'
        self.assertEqual(response.status_code, 302, msg)

    def test_post_delete_test_checkpoint(self):
        """POST to the TestCheckpoint index.html (Delete Test Checkpoint).
        """
        # First, POST to the REST API.
        test_data = data_generator(10)
        node_data = {'uid': self._mac,
                     'role': 'client'}
        r = self._c.post(self._checkpoint_uri,
                         data=json.dumps({'node': node_data,
                                          'data': test_data}),
                         content_type='application/json')

        # Query the DB directly to ensure that it exists.
        instance = Checkpoint.objects.get(data=test_data)

        # Now delete it.
        request_post = {u'submit': [u'test_checkpoint_del_pk_%d' %
                                    instance.pk]}
        r = self._c.post('/testcheckpoint/delete/', request_post)
        msg = 'Checkpoint POST to delete status_code not 304 (Redirect)'
        self.assertEqual(r.status_code, 302, msg)

        # Finally, check the database.
        with self.assertRaises(Checkpoint.DoesNotExist):
            Checkpoint.objects.get(data=test_data)

    @classmethod
    def tearDownClass(cls):
        cls._c = None
        cls._mac = None
        cls._checkpoint_uri = None
