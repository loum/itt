__all__ = [
    "ServerConfig",
    "list",
]

import ConfigParser
import io

import itt

def list():
    """Display parsed configuraton items to stdout.

    For example:

        >>> from itt.server.config import list
        >>> itt.server.config.list()
        Section: ftp
        Options: ['root', 'port', 'pidfile']
        root = /tmp
        port = 2121
        pidfile = /tmp/ittserverd.ftp.pid
        ...

    """
    c = itt.ServerConfig()
    for section_name in c.config.sections():
        print('Section: %s' % section_name)
        print('\tOptions: %s' % c.config.options(section_name))
        for name, value in c.config.items(section_name):
            print('\t%s = %s' % (name, value))
        print


class ServerConfig(object):
    """Limit the ITT server definitions into one place.

    The configuration structure is built on top of :mod:`ConfigParser`
    module and follows the same section/items based principle.  For
    example, the ITT variant of the configuration for an FTP server is:

        # This is valid ConfigParser syntax:
        [ftp]  # section header
        root = /tmp  #items
        port = 2121
        pidfile = /tmp/ittserverd.ftp.pid

    To access the FTP configuration settings, create an :mod:`itt.ServerConfig`
    object as follows:

        >>> import itt
        >>> c = itt.ServerConfig(server='ftp')
        ...

    To slurp all of the section items into a handy dictionary:

        >>> c.kwargs
        {'root': '/tmp', 'port': '2121', 'pidfile': ... }
        ...

    .. note::

        TODO - we need a better config strategy around the settings
        strategy ...

    An example of how to access the Config items is as follows:

    >>> import itt
    >>> c = itt.ServerConfig(server='ftp')

    The defined attributes are:

    .. attribute:: server (string)

        The type of controlling server in this instance.  Supported types:

        * ``ftp`` for FTP
        * ``tftp`` for TFTP
        * ``http`` for HTTP

    .. attribute:: server_types (dict)

        A dictionary of ``server``'s whose items are a tuple in the form
        (<module_name>, <class_name>) and can be plugged in directly into
        the the :func:`getattr` function.

    .. attribute:: lookup

        Handy getter that returns a (<module_name>, <class_name>) pair
        based on the current controlling *server*

    .. attribute:: settings

        Ugly, hardwired raw config settings.  Not some of my best work.

    .. attribute:: config (:class:`ConfigParser.RawConfigParser`)

        A :class:`ConfigParser.RawConfigParser` object that provides
        a handle to the individual elements of the configuration.

    .. attribute:: kwargs (dict)    

        Handy getter property attribute that returns the required
        argument list that feeds directly into :class:`itt.Server` class
        constructor.

    """
    def __init__(self, server=None):
        """In theory, all supported ITT servers need to be listed here in
        the format that will keep :func:`getattr` happy.

        """
        self._server = server
        self._config = None
        self._server_types = {'http': (itt.server.httpserver, 'HttpServer'),
                              'ftp': (itt.server.ftpserver, 'FtpServer'),
                              'tftp': (itt.server.tftpserver, 'TftpServer')}

        # Ugly, ugly, fugly ...
        self._settings = """
[ftp]
root = /tmp
port = 2121
pidfile = /tmp/ittserverd.ftp.pid
[tftp]
root = /tmp
port = 6969
pidfile = /tmp/ittserverd.tftp.pid
[http]
root = /tmp
port = 8000
pidfile = /tmp/ittserverd.http.pid"""

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, value):
        self._server = value

    @property
    def server_types(self):
        return self._server_types

    @property
    def lookup(self):
        return self.server_types[self._server]

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = value

    @property
    def config(self):
        if self._config is None:
            self._parse_config()

        return self._config

    @property
    def kwargs(self):
        return dict(self.config.items(self._server))

    @config.setter
    def config(self, value):
        self._config = value

    def _parse_config(self):
        """Create a configuration lookup based on settings that can
        be provided via a file or inline.

        """
        self.config = ConfigParser.RawConfigParser()
        self.config.readfp(io.BytesIO(self.settings))
