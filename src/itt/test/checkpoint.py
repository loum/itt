""":mod:`itt.test.checkpoint` defines an ITT test checkpoint.
"""

__all__ = [
    "TestCheckpoint",
]

import requests
import json
import uuid
import re

from itt.utils.log import log, class_logging


@class_logging
class TestCheckpoint(object):
    """TestCheckpoint initialisation.

    .. note::

        All public attribute access is implemented in a Pythonic property
        decorator style.

    .. attribute:: name

        A user-friendly name of the resource that generates the checkpoint.

    .. attribute:: uid

        A machine-friendly name of the resource that generates the
        checkpoint.

    .. attribute:: payload

        Data structure that maintains the information that will be sent
        to the resource.  Implemented as a Python dictionary.

        Typical construct as follows::

            {'uid': '08:00:27:9F:F4:CC', }

    .. attribute:: url

        The remote address that will consume the checkpoint message.

        .. note::

            Leave blank to assume a standalone IIT instance in which case
            the resource will publish locally.

    """
    def __init__(self,
                 name=None,
                 uid=None,
                 url=None,
                 payload=None,
                 headers=None):
        """
        """
        self._name = name
        self._uid = uid
        self._url = url
        self._payload = payload 
        self._headers = headers 

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def uid(self):
        if self._uid is None:
            self._uid = ':'.join(re.findall('..', '%012x' % uuid.getnode()))

        return self._uid

    @uid.setter
    def uid(self, value):
        self._uid = value

    @property
    def payload(self):
        if self._payload is None:
            self._payload = {'uid': self.uid, }

        return self._payload

    @payload.setter
    def payload(self, value):
        # TODO: some validation ???
        self._payload = value
    
    @property
    def url(self):
        if self._url is None:
            # Assume standalone.
            self._url = 'http://127.0.0.1:8080/test/checkpoint/'

        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def headers(self):
        if self._headers is None:
            self._headers = {'content-type': 'application/json'}

        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = value

    def commit(self):
        """Send to the resource.
        """
        r = requests.post(self.url,
                          data=json.dumps(self.payload),
                          headers=self.headers)
        log.debug('POST response: %s' % r.text)

        return r.text
