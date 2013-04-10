"""The :mod:`itt.utils.daemon` module aims to provide the functionality
to support daemonisation of a process.

.. note::

    Bulk of this code was taken from http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/ with some re-work.

"""
__all__ = [
    "Daemon",
    "DaemonError",
]

import sys
import os
import atexit
import signal
from abc import ABCMeta, abstractmethod

from itt.utils.log import log, class_logging
from itt.utils.files import is_writable
 

@class_logging
class Daemon(object):
    """A generic daemon class.
    
    :class:`Daemon` will prepare the daemon environment for you but
    expects that you give it an entry point (:method:`run`) to the
    functional component of your process.

    The following example shows a trivial class that defines a :method:`run`
    method ...

    >>> import itt.utils
    >>> import time
    >>> class DummyDaemon(itt.utils.Daemon):
    >>>     def run(self):
    >>>         while True:
    >>>             time.sleep(5)
    >>>
    >>> d = DummyDaemon(pidfile='/tmp/my_dummy_pid')
    >>> d.start()
    ...

    To stop:
    >>> d.stop()

    The :method:`start` method manages the daemonisation of the environment
    and makes the actual call to your own instance of the :method:`run`
    method.

    """
    __metaclass__ = ABCMeta

    def __init__(self,
                 pidfile=None,
                 stdin='/dev/null',
                 stdout='/dev/null',
                 stderr='/dev/null',
                 term_parent=True):
        """Daemon class initialiser.

        :class:`Daemon` is built on top the the :mod:`abc` Abstract Base
        Class module and is defined as *abstract*.  It is not intended to
        be instantiated directly.  Instead, it forces generalisations
        to define their own :method:`run` method.  :method:`run`
        will be called after the process has been daemonised by
        :method:`start` or :method:`restart`.

        :class:`Daemon` expects the caller to define a *pidfile*.  Otherwise
        the *pidfile* will default to ``None`` and all deamonisation will
        be suppressed.  Any attempts to call methods without a *pidfile*
        will raise an exception.

        **Kwargs:**
            pidfile (str): Path to the PID file.  Default to ``None``.

            term_parent (boolean): Attempt to terminate the parent to
            enforce true separation between parent and child processes.
            Useful when running under test scenarios as :mod:`unittest2`
            barfs if you try to kill it.  Defaults to ``True``.

        **Raises:**
            IOError if *pidfile* is not writable.

        """
        self._pidfile = pidfile
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self._term_parent = term_parent

        self.pid = None
        self.pidfs = None

        # Only validate settings if a pidfile was specified.
        if self.pidfile is not None:
            self._validate()

    @property
    def pidfile(self):
        return self._pidfile

    @pidfile.setter
    def pidfile(self, value):
        self._pidfile = value

    @property
    def term_parent(self):
        return self._term_parent

    @abstractmethod
    def run(self): pass

    def _validate(self):
        """Validator method called during object initialisation.

        ..note::

            When starting a new process, the PID file will be relative
            to '/' once the process is forked.
        """
        if not os.path.isabs(self.pidfile):
            self._debug('PID file "%s" is relative -- make absolute' %
                        self.pidfile)
            self.pidfile = os.path.join(os.sep, self.pidfile)
            self._debug('PID file now "%s"' % self.pidfile)

        # Check if the PID file exists.
        if os.path.exists(self.pidfile):
            # PID file exists, so the process may be active.
            # Set the current process PID.
            self._debug('PID file "%s" exists' % self.pidfile)
            self.pid = file(self.pidfile, 'r').read().strip()
            self._debug('Stored PID is: %s' % self.pid)
        else:
            # PID file is missing -- process is idle.
            # Check if writable to save hassles later on.
            self._debug('No PID file -- creating handle')
            self.pidfs = is_writable(self.pidfile)

    def start(self):
        """Start the daemon process.

        ..note::

            Daemon will only start if PID file does not exist.

        The :method:`start` method checks for an existing PID before
        preparing the daemon environment.  Finally, it will initiate
        the daemon process run sequence.

        **Returns:**
            boolean::

                ``True`` -- success
                ``False`` -- failure

        **Raises:**
            DaemonError

        """
        start_status = False

        if self.pidfile is None:
            raise DaemonError('PID file has not been defined')

        self._debug('checking daemon status with PID: "%s"' % self.pid)
        if self.pid is not None:
            msg = ('PID file "%s" exists.  Daemon may be running?\n' %
                   self.pidfile)
            log.error(msg)
        else:
            # So far, so good -- start the daemon.
            self._debug('starting daemon')
            self.daemonize()
            self.run()
            start_status = True

        return start_status 
 
    def daemonize(self):
        """Prepare the daemon environment.

        Does the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177).

        The second child PID is written out to the PID file.  This acts
        as a persistent state check, where no file implies that the
        daemon process is idle.

        The daemon process environment acts as a container for your process
        logic.  As such, once the daemon process ends it will remove its
        associated PID file automatically.

        """
        self._debug('attempting first fork')
        try:
            pid = os.fork()

            # Exit first parent.
            if pid > 0:
                if self.term_parent:
                    sys.exit(0)
                else:
                    return
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno,
                                                            e.strerror))
            sys.exit(1)

        # Decouple from parent environment.
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # Do second fork.
        try:
            pid = os.fork()

            # Exit from second parent.
            if pid > 0:
                if self.term_parent:
                    sys.exit(0)
                else:
                    return
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno,
                                                            e.strerror))
            sys.exit(1)

        # Redirect standard file descriptors.
        if self.term_parent:
            sys.stdout.flush()
            sys.stderr.flush()
            si = file(self.stdin, 'r')
            so = file(self.stdout, 'a+')
            se = file(self.stderr, 'a+', 0)
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())

        # Write out to pidfile.
        child_pid = str(os.getpid())
        self._debug('PID of child process: %s' % child_pid)
        file(self.pidfile, 'w+').write("%s\n" % child_pid)

        # Remove the PID file when the process terminates.
        atexit.register(self._delpid)
 
    def stop(self):
        """Stop the daemon.

        Will run a series of checks around the existence of a PID file
        before attempting to terminate the daemon.

        **Returns:**
            boolean::

                ``True`` -- success
                ``False`` -- failure

        """
        stop_status = False

        if self.pid:
            # OK to terminate.
            self._debug('stopping daemon process with PID: %s' % self.pid)
 
            try:
                os.kill(int(self.pid), signal.SIGTERM)
            except OSError as err:
                log.warn('err: %s' % str(err))
                log.warn('PID "%s" does not exist' % self.pid)
                if err.errno == 3:
                    log.warn('Removing PID file "%s"' % self.pidfile)
                    if os.path.exists(self.pidfile):
                        os.remove(self.pidfile)
            else:
                stop_status = True
        elif self.pid is None:
            # PID file does not exist.
            log.warn('Stopping process but PID file is missing')
            self._cleanup()
        else:
            # Should not happen, but ...
            log.warn('PID file exists with invalid value: "%s"' %
                     str(self.pid))

        return stop_status
 
    def restart(self):
        """Restart the daemon

        No real magic here -- simply calls the :method:`stop` and
        :method:`start` method sequence (in that order)

        .. TODO::

            Need better tests around this process.

        """
        self.info('attempting daemon restart')
        if self.stop():
            log._debug('stop OK -- trying start ...')
            self.start()

    def _delpid(self):
        """Simple wrapper method around file deletion.
        """
        os.remove(self.pidfile)

    def _cleanup(self):
        """
        """
        self.pidfs.close()
        os.remove(self.pidfile)

    def _debug(self, log_msg):
        """Wrapper method around the debug logging level which adds a bit
        more verbose information.
        """
        name = "%s.%s" % (type(self).__module__, type(self).__name__)
        log.debug('%s - %s' % (name, log_msg))


class DaemonError(Exception):
    """Standard exception for a Daemon error.

    Very simplistic at the moment in that it only caters for situations
    where functionality is requested without a valid PID file specified.

    .. attribute:: msg

        An explanation of the error.

    """
    def __init__(self, value):
        self.msg = value

    def __str__(self):
        return repr(self.msg)
