import re
import uuid
import json
from django.test import TransactionTestCase
from django.test.client import Client

from test_checkpoint.models import Node


class TestTestNode(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        # Get a some kind of unique representation for the node via MAC.
        cls._mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        cls._c = Client()

    def test_post_new_node_with_data(self):
        """POST request to the Node resource with node data.
        """
        r = self._c.post('/test/node/',
                         data=json.dumps({'uid': self._mac}),
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
        node = Node.objects.get(pk=pk)
        msg = 'Database query for POST Node.data mismatch'
        received = node.uid
        expected = self._mac
        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        cls._mac = None
