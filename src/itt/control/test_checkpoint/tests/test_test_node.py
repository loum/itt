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

    def test_post(self):
        """Test a POST request to the Node resource.
        """
        response = self._c.post('/test/node/',
                                data=json.dumps({'uid': self._mac}),
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
        r = Node.objects.get(pk=pk)
        msg = 'Database query for POST data mismatch'
        received = r.uid.encode('ascii')
        expected = self._mac
        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        cls._mac = None
