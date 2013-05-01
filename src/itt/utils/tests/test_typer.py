import unittest2

from itt.utils.typer import bool_check

class Bogus(object):
    def __init__(self):
        self._bool_var = False

    @property
    def bool_var(self):
        return self._bool_var

    @bool_var.setter
    @bool_check
    def bool_var(self, value):
        self._bool_var = value

class TestTyper(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._bogus = Bogus()

    def test_bool_check_with_int(self):
        """Try and assign an integer to a bool.
        """
        with self.assertRaises(TypeError):
            self._bogus.bool_var = 0

    def test_bool_check_with_string(self):
        """Try and assign a string to a bool.
        """
        with self.assertRaises(TypeError):
            self._bogus.bool_var = 'string'

    def test_bool_check_with_none_type(self):
        """Try and assign a none type to a bool.
        """
        with self.assertRaises(TypeError):
            self._bogus.bool_var = None

    def test_bool_check_with_valid_assignment(self):
        """Try and assign a valid bool.
        """
        msg = 'Bool assignment should honor value and not raise exception'
        self._bogus.bool_var = False
        self.assertFalse(self._bogus.bool_var, msg)

        self._bogus.bool_var = True
        self.assertTrue(self._bogus.bool_var, msg)

    @classmethod
    def tearDownClass(cls):
        cls._bogus = None
