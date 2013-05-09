from django.test import TransactionTestCase

import common.utils


class TestCommonUtils(TransactionTestCase):

    def test_parse_pk_valid_edit_input_value(self):
        """Valid parse of a test_config edit input value.
        """
        input_value = 'test_config_edit_pk_2'
        received = common.utils.parse_pk(input_value)
        expected = 2
        msg = ('Primary key parse of "%s" did not return %d' %
               (input_value, received))
        self.assertEqual(received, expected, msg)

    def test_parse_pk_invalid_edit_input_value(self):
        """Invalid parse of a test_config edit input value.
        """
        input_value = 'test_config_edit_pk_'
        received = common.utils.parse_pk(input_value)
        msg = 'Primary key parse of "%s" did not return None' % input_value
        self.assertIsNone(received, msg)

