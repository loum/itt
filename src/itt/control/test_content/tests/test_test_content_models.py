from django.test import TransactionTestCase
from django.core.exceptions import ValidationError

from itt.control.test_content.models import TestContent


class TestTestContentModels(TransactionTestCase):

    def test_init(self):
        """Test initalisation of the TestContent model.
        """
        tc = TestContent()
        msg = 'Did not receive a TestContent object'
        self.assertIsInstance(tc, TestContent, msg)

    def test_init_bytes_field_below_range(self):
        """Test TestContent.bytes field minimum value.
        """
        tc = TestContent(name='tester',
                         bytes=-100)
        with self.assertRaises(ValidationError):
            tc.clean_fields()
