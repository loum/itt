import re
import uuid
import json
from django.db import connection
from django.test import TestCase
from django.test.client import Client
from django.test.utils import (setup_test_environment,
                               teardown_test_environment)

import itt

#import settings

class TestTestCheckpoint(TestCase):

    @classmethod
    def setUpClass(cls):
        setup_test_environment()
        connection.creation.create_test_db(0)

        cls._uid = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        cls._c = Client()

    def test_init(self):
        """Simple initialisation of TestCheckpoint object with no values.
        """
        chkp = itt.TestCheckpoint()
        msg = 'Object is not a TestCheckpoint'
        self.assertIsInstance(chkp, itt.TestCheckpoint, msg)

    def test_check_uid(self):
        """Empty initialisation "uid" check.
        """
        # Note: may fail if system has more than one NIC.
        chkp = itt.TestCheckpoint()
        msg = "TestCheckpoint uid should return auto-generated value"
        self.assertEqual(chkp.uid, self._uid, msg)

#    def test_commit(self):
#        """Simulate a POST request with constructed data.
#        """
#        # Note: we can actually use the commit method here because we
#        # don't have an operational REST API.  Instead, we'll fake it with
#        # Django's test client.  At least, we can verify the payload ???
#        chkp = itt.TestCheckpoint()
#
#        r = self._c.post(chkp.url,
#                         data=json.dumps(chkp.payload),
#                         content_type='application/json')
#
#        # Check the response code.
#        received = r.status_code
#        expected = 201
#        msg = 'POST response not 201 -- received %s' % received
#        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        connection.creation.destroy_test_db(':memory:', 0)
        teardown_test_environment()
        cls._uid = None
        cls._c = None
