import unittest2

from utils.log import log

class TestLog(unittest2.TestCase):

    def test_log(self):
        """Test the log facility.
        """
        log.debug("debug message")
        log.error("error message")
