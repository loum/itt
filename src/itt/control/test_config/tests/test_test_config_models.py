from django.test import TransactionTestCase
from django.core.exceptions import ValidationError

from itt.control.test_config.models import TestConfig


class TestTestConfigModels(TransactionTestCase):

    def test_init(self):
        """Test initalisation of the TestConfig model.
        """
        test_config = TestConfig()
        msg = 'Did not receive a TestConfig object.'
        self.assertTrue(isinstance(test_config, TestConfig), msg)

    def test_init_bytes_field_below_range(self):
        """Test TestConfig.bytes field minimum value.
        """
        test_config = TestConfig(bytes=-1)
        with self.assertRaises(ValidationError):
            test_config.clean_fields()

    def test_init_minimum_gap_field_below_range(self):
        """Test TestConfig.minimum_gap field minimum value.
        """
        test_config = TestConfig(minimum_gap=-1)
        with self.assertRaises(ValidationError):
            test_config.clean_fields()
