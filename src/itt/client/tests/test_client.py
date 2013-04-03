import unittest2
import itt

class TestClient(unittest2.TestCase):

    def test_init(self):
        """Test constructon of the IP Test Tool base Client class.
        """
        self.assertRaises(TypeError, itt.Client)
