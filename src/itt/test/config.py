__all__ = [
    "TestConfig",
]

from types import *

from itt.utils.log import log, class_logging
from itt.utils.typer import (bool_check,
                             int_check,
                             not_none_check)

@class_logging
class TestConfig(object):
    """Test Configuration...

    XXX: Todo: Doco!

    """
    def __init__(self, host, port, protocol,
                 upload=None,
                 bytes=None,
                 content=None,
                 minimum_gap=None,
                 chunk_size=None,
                ):
        ##  enums...
        self.VALID_PROTOCOLS = [
            'http',
            'ftp',
            'tftp',
        ]

        ##  properties
        self.host = host
        self.port = port
        self.upload = upload
        self.bytes = bytes
        self.content = content
        self.protocol = protocol
        self.minimum_gap = minimum_gap
        self.chunk_size = chunk_size

    def __repr__(self):
        return "<TestConfig host:%s port:%s protocol:%s upload:%s bytes:%s content:%s minimum_gap:%s chunk_size:%s>" % (
            self.host,
            self.port,
            self.protocol,
            self.upload,
            self.bytes,
            self.content,
            self.minimum_gap,
            self.chunk_size,
            )
    
    
    ##--host
    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        if type(value) is str:
            self._host = value
        else:
            ## XXX: throw a proper ITT exception?
            msg = "Host should be provided as a string (either hostname or IP)"
            log.error(msg)
            raise Exception(msg)


    ##--port
    @property
    def port(self):
        return self._port

    @port.setter
    @int_check(greater_than=0, less_than=65536)
    @not_none_check
    def port(self, value):
        #MAX_PORT = 65535
        self._port = value

    
    ##--netloc
    ##   -> is the combination of host and port as "host:port"
    @property
    def netloc(self):
        return "%s:%s" % (
            self.host,
            self.port,
        )


    ##--upload
    @property
    def upload(self):
        return self._upload

    @upload.setter
    @bool_check
    def upload(self, value):
        self._upload = value

    ##--bytes
    @property
    def bytes(self):
        return self._bytes

    @bytes.setter
    @int_check(greater_than=1)
    def bytes(self, value):
        self._bytes = value

    ##--content
    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value


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


    ##--minimum_gap
    @property
    def minimum_gap(self):
        return self._minimum_gap

    @minimum_gap.setter
    def minimum_gap(self, value):
        if type(value) is NoneType:
            self._minimum_gap = value
        else:
            try:
                float(value)
            except:
                ## XXX: convert to a ITT exception?
                msg = "Invalid minimum gap (must be a float)"
                log.error(msg)
                raise Exception(msg)

            if float(value) > 0:
                self._minimum_gap = value
            else:
                ## XXX: throw a proper ITT exception?
                msg = "Invalid minimum gap"
                log.error(msg)
                raise Exception(msg)


    ##--chunk_size
    @property
    def chunk_size(self):
        return self._chunk_size

    @chunk_size.setter
    @int_check(greater_than=0)
    def chunk_size(self, value):
        self._chunk_size = value
