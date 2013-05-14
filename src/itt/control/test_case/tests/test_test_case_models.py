from django.test import TransactionTestCase

from control.test_case.models import TestCase


class TestTestCaseModels(TransactionTestCase):

    def test_init(self):
        """Initialise te TestCase model.
        """
        tc = TestCase()
        msg = 'Did not receive a TestCase model.'
        self.assertIsInstance(tc, TestCase, msg)
