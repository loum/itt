import json
from django.test import TransactionTestCase
from django.test.client import Client

from test_checkpoint.models import Checkpoint
from itt.utils.files import data_generator


class TestTestCheckpoint(TransactionTestCase):

    fixtures = ['test_node']

    @classmethod
    def setUpClass(cls):
        cls._mac = '00:11:22:33:44:55'
        cls._c = Client()
        cls._node_uri = '/test/node/1/'
        cls._data = data_generator(10)
        cls._checkpoint_uri = '/test/checkpoint/'

    def test_post(self):
        """Test a POST request to the Checkpoint resource.
        """
        # First, we need to have an entry in the Node table.
        response = self._c.post(self._checkpoint_uri,
                                data=json.dumps({'node': self._node_uri,
                                                 'data': self._data}),
                                content_type='application/json')

        # Check the response code.
        received = response.status_code
        expected = 201
        msg = 'POST response not 201 -- received %s' % received
        self.assertEqual(received, expected, msg)

        # Capture the response.
        #
        # Content comes through as a string object.
        # Try to convert into a dict object.
        content = response.content
        dict_content = json.loads(content, encoding='UTF-8')
        pk = dict_content['id']

        # Check the database.
        r = Checkpoint.objects.get(pk=pk)
        msg = 'Database query for POST data mismatch'
        received = r.data.encode('ascii')
        expected = self._data
        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        cls._mac = None
        cls._c = None
        cls._node_uri = None
        cls._data = None
        cls._checkpoint_uri = None
