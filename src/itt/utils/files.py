__all__ = [
    "RenamedTemporaryFile",
    "dummy_filesystem",
    "is_writable",
]

import os.path
import tempfile
from log import log

def is_writable(path):
    """Handy sugar function to check if the invoking user has write access
    to *path*.

    **Args:**
        path (str): Path to the file name to check access to.

    **Returns:**
        object of the :mod:`file` type on success or ``None``.

    """
    try:
        fh = open(path, 'w')
    except IOError:
        raise
    else:
        return fh

def dummy_filesystem(content=None):
    """Not much to see here unless you're looking for a dummy
    filesystem to use in your tests ???

    Based on the NamedTemporaryFile module, will automatically
    create an absolute file path to a unique file.

    Exploits closures to manage file cleanup -- file deletion is done for
    you.

    .. note::

       Would love to extend to this to handle multiple nested files and
       directories.

    **Args:**
        content (str): Stuff that you want in the test file.

    **Returns:**
        temp_file: tempfile.NamedTemporaryFile object
    """
    temp_file = tempfile.NamedTemporaryFile()

    if content is not None:
        with open(temp_file.name, 'w') as fh:
            fh.write(content)

    return temp_file

class RenamedTemporaryFile(object):
    """Input/output file handle manager.

    RenamedTemporyFile takes care of file handle creation and tear down.
    Handy if you just want to write to a file in a particular directory
    without having to worry about boring (yawn) file details.

    .. note::

       Your nominated directory must exist.  Otherwise, file will just be
       created in the current directory.

    When used within context of a ``with`` statement, will return an object
    of the file type and pass it to the variable defined by ``as`` clause.
    File handle is closed when the ``with`` exits.

    .. note::

        Although built on the tempfile.NamesTemporyFile module, filename
        has been set to persist after file handle closure.

    Example usage as follows ...

    Say I want to write to the persistent file, ``banana``:

    >>> with RenamedTemporaryFile("banana") as f:
    >>>     f.write("stuff")

    """

    def __init__(self, final_path, **kwargs):
        """Initialise a RenamedTemporaryFile object.

        **Args:**
            final_path (str): The resultant filename.

        **Kwargs:**
            kwargs: same as the kwargs for
            :mod:`tempfile.NamedTemporaryFile`

        """
        tmpfile_dir = kwargs.pop('dir', None)

        # To ensure atomic move of the final file, put the temporary file
        # into the same directory as the location of the final file.
        if tmpfile_dir is None:
            tmpfile_dir = os.path.dirname(final_path)

        self.tmpfile = tempfile.NamedTemporaryFile(dir=tmpfile_dir,
                                                   **kwargs)
        self.final_path = final_path

    def __getattr__(self, attr):
        """Delegate attribute access to the underlying temporary file
        object.
        """
        return getattr(self.tmpfile, attr)

    def __enter__(self):
        log.debug('Preparing to write "%s"' % self.tmpfile.name)
        self.tmpfile.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_traceback):
        if exc_type is None:
            # No problems with file write so rename the file.
            self.tmpfile.delete = False
            result = self.tmpfile.__exit__(exc_type, exc_val, exc_traceback)
            os.rename(self.tmpfile.name, self.final_path)
        else:
            result = self.tmpfile.__exit__(exc_type, exc_val, exc_traceback)

        return result
