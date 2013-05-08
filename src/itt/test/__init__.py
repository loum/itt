""":mod:`itt.test` encapsulates the settings that make up a ITT test
   case: *TestConfig*, *TestConnection*, and *TestContent*.
"""

__all__ = [
    "Test",
]

from itt.utils.log import log, class_logging


@class_logging
class Test(object):
    """IP Test Tool base test class.

    Current thinking (at 2013-05-07):
    t = itt.Test(itt.test.config, itt.test.content, itt.test.connection)
    t.execute()
    t.reportRestuls()
    """

    def __init__(self, config, content, connection):

        self.config = config
        self.content = content
        self.connection = connection


    ##--properties

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, value):
        self._connection = value
