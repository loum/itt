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

    def test_post_with_existing_node_uri(self):
        """Test a POST request to the Checkpoint resource.
        """
        # This test relies on an existing entry in the Node table.
        test_data = data_generator(10)
        r = self._c.post(self._checkpoint_uri,
                         data=json.dumps({'node': self._node_uri,
                                          'data': test_data}),
                         content_type='application/json')

        # Check the response code.
        received = r.status_code
        expected = 201
        msg = 'POST response not 201 -- received %s' % received
        self.assertEqual(received, expected, msg)

        # Capture the response (comes through as string).
        content_dict = json.loads(r.content, encoding='UTF-8')
        pk = content_dict['id']

        # Check the database.
        r = Checkpoint.objects.get(pk=pk)
        msg = 'Database query for POST data mismatch'
        received = r.data.encode('ascii')
        expected = test_data
        self.assertEqual(received, expected, msg)

    def test_post_existing_node_provided_via_data(self):
        """POST request which targets an existing Node via data entry.
        """
        test_data = data_generator(10)
        node_data = {'uid': self._mac,
                     'role': 'client'}
        r = self._c.post(self._checkpoint_uri,
                         data=json.dumps({'node': node_data,
                                          'data': test_data}),
                         content_type='application/json')

        # Check the response code.
        received = r.status_code
        expected = 201
        msg = 'POST response not 201 -- received %s' % received
        self.assertEqual(received, expected, msg)

        # Capture the response (comes through as string).
        content_dict = json.loads(r.content, encoding='UTF-8')

        # Check that the node picks up the existing entry in the Node table.
        expected = '/test/node/1/'
        received = content_dict['node']
        msg = 'URI of node foriegn key is not "%s"' % expected
        self.assertEqual(expected, received, msg)

        # Check the database.
        c = Checkpoint.objects.get(data=test_data)
        received = c.data
        expected = test_data
        msg = 'Database query after POST Checkpoint.data mismatch'
        self.assertEqual(received, expected, msg)

        received = c.pk
        expected = 1
        msg = 'Database query after POST Checkpoint.pk mismatch'
        self.assertEqual(received, expected, msg)

        test_data = data_generator(10)
        node_data = {'uid': self._mac,
                     'role': 'client'}
        r = self._c.post(self._checkpoint_uri,
                         data=json.dumps({'node': node_data,
                                          'data': test_data}),
                         content_type='application/json')

        # Check the response code.
        received = r.status_code
        expected = 201
        msg = 'POST response not 201 -- received %s' % received
        self.assertEqual(received, expected, msg)

        # Check the database.
        c = Checkpoint.objects.get(data=test_data)
        received = c.data
        expected = test_data
        msg = 'Database query after 2nd POST Checkpoint.data mismatch'
        self.assertEqual(received, expected, msg)

        # The Checkpoint row count should have incremented by 1.
        received = c.pk
        expected = 2
        msg = 'Database query after 2nd POST Checkpoint.pk mismatch'
        self.assertEqual(received, expected, msg)

        # The Node id should remain the same.
        received = c.node.id
        expected = 1
        msg = 'Database query after 2nd POST Checkpoint.node mismatch'
        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        cls._mac = None
        cls._c = None
        cls._node_uri = None
        cls._data = None
        cls._checkpoint_uri = None
