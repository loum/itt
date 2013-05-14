from django.test import TransactionTestCase
from django.core.exceptions import ValidationError

from control.test_connection.models import TestConnection


class TestTestConnectionModels(TransactionTestCase):

    def setUp(self):
        self._dummy_data = {'name': 'tester',
                            'host': 'localhost',
                            'port': '1234',
                            'protocol': 'ftp', }

    def test_init(self):
        """Test initialisation of the TestConnection model.
        """
        tc = TestConnection()
        msg = 'Did not receive a TestConnection object.'
        self.assertIsInstance(tc, TestConnection, msg)

    def test_init_with_valid_values(self):
        """Initialisation of the TestConnection with valid data.
        """
        tc = TestConnection(**self._dummy_data)
        msg = 'Did not receive a TestConnection object.'
        self.assertIsInstance(tc, TestConnection, msg)

    def test_init_port_field_below_range(self):
        """Test TestConnection.port field minimum value.
        """
        # Override the dummy data with invalids.
        self._dummy_data['port'] = 0
        tc = TestConnection(**self._dummy_data)
        with self.assertRaises(ValidationError) as cm:
            tc.clean_fields()

        exception = cm.exception
        self.assertEqual(exception.message_dict['port'][0],
                         'Ensure this value is greater than or equal to 1.')

    def test_init_port_field_above_range(self):
        """Test TestConnection.port field maximum value.
        """
        # Override the dummy data with invalids.
        self._dummy_data['port'] = 70000
        tc = TestConnection(**self._dummy_data)
        with self.assertRaises(ValidationError) as cm:
            tc.clean_fields()

        exception = cm.exception
        expected = 'Ensure this value is less than or equal to 65535.'
        self.assertEqual(exception.message_dict['port'][0], expected)

    def test_init_protocol_invalid_choice(self):
        """Test TestConnection.protocol invalid choice.
        """
        # Override the dummy data with invalids.
        self._dummy_data['protocol'] = 'banana'
        tc = TestConnection(**self._dummy_data)
        with self.assertRaises(ValidationError) as cm:
            tc.clean_fields()

        exception = cm.exception
        expected = "Value 'banana' is not a valid choice."
        self.assertEqual(exception.message_dict['protocol'][0], expected)

    @classmethod
    def tearDown(self):
        self._dummy_data = None
