import unittest2

import itt


class TestTestConfig(unittest2.TestCase):

    def test_init(self):
        """Test construction of the IP Test Tool TestConfig class.
        """
        itt.TestConfig()
