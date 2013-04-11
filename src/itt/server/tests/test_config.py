import unittest2

import itt


class TestConfig(unittest2.TestCase):

    def test_init_no_args(self):
        """Test initialisation with no arguments.
        """
        with self.assertRaises(TypeError):
            itt.Config()
