import unittest2

import itt

class TestTestContent(unittest2.TestCase):

    def test_init_with_no_args(self):
        """Test construction of the TestContent class with no args.
        """
        itt.TestContent()
