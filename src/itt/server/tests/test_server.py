import unittest2
import itt

class TestServer(unittest2.TestCase):

    def test_init(self):
        """Test construction of the IP Test Tool base Server class.
        """
        self.assertRaises(TypeError, itt.Server)
