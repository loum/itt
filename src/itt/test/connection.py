""":mod:`itt.test.connnection` defines the connections settings for ITT
test cases.
"""

__all__ = [
    "TestConnection",
]

from itt.utils.log import log, class_logging
from itt.utils.typer import (bool_check,
                             int_check,
                             float_check,
                             not_none_check)


@class_logging
class TestConnection(object):
    """Test Connection...

    .. note::

        All public attribute access is implemented in a Pythonic property
        decorator style.

    .. attribute:: host

    .. attribute:: port

    .. attribute:: protocol

        Must be one of *http*, *ftp*, or, *tftp*.

    .. attribute:: netloc

        Property getter which returns a ``string`` object representing a
        combination of host and port as ``host:port``
    """

    def __init__(self, host, port, protocol):
        ##  enums...
        self.VALID_PROTOCOLS = [
            'http',
            'ftp',
            'tftp',
        ]

        ##  properties
        self.host = str(host)
        self.port = int(port)
        self.protocol = str(protocol)

    def __repr__(self):
        return "<TestConnection host:%s port:%s protocol:%s>" % (
            self.host,
            self.port,
            self.protocol,
        )

    ##--host
    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    ##--port
    @property
    def port(self):
        return self._port

    @port.setter
    @int_check(greater_than=0, less_than=65536)
    @not_none_check
    def port(self, value):
        self._port = value

    ##--netloc
    @property
    def netloc(self):
        return "%s:%s" % (
            self.host,
            self.port,
        )

    ##--protocol
    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        try:
            if value.lower() in self.VALID_PROTOCOLS:
                self._protocol = value.lower()
            else:
                raise Exception()
        except:
            ## XXX: throw a proper ITT exception?
            msg = "Invalid protocol"
            log.error(msg)
            raise Exception(msg)
