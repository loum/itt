import unittest2

import itt


class TestConfig(unittest2.TestCase):

    def test_parse_config(self):
        """Test initial parsing of the configuration settings.
        """
        c = itt.Config(server='ftp')

        # Override the settings attribute with some bogus data.
        c.settings = """
[bogus]
item01 = item01 value
item02 = item02 value
"""

        # First call to config property attribute will parse settings.
        msg = 'Bogus config section value for "item01" incorrect'
        received = c.config.get('bogus', 'item01')
        expected = 'item01 value'
        self.assertEqual(received, expected, msg)

    def test_call_missing_section(self):
        """Test call to a missing configuration section.
        """
        c = itt.Config()
        c.server = 'bogus'
        with self.assertRaises(KeyError):
            c.lookup
