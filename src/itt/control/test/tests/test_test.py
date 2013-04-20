import json
from django.test import TestCase
from django.test.client import Client

from test.models import Checkpoint


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class TestCheckpoint(TestCase):

    def test_post(self):
        """Test a POST request to the resource.
        """
        c = Client()
        response = c.post('/test/checkpoint/',
                          data=json.dumps({'data' : 'data003'}),
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
        expected = 'data003'
        self.assertEqual(received, expected, msg)
