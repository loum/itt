import unittest2
import random

from itt.utils.typer import (bool_check,
                             int_check,
                             not_none_check)

class Bogus(object):
    def __init__(self):
        self._bool_var = False
        self._int_var_gt = 0
        self._int_var_lt = 0
        self._not_none_var = 0
        self._int_not_none_var = 0

    @property
    def bool_var(self):
        return self._bool_var

    @bool_var.setter
    @bool_check
    def bool_var(self, value):
        self._bool_var = value

    @property
    def int_var(self):
        return self._int_var

    @int_var.setter
    @int_check()
    def int_var(self, value):
        self._int_var = value

    @property
    def int_var_gt(self):
        return self._int_var_gt

    @int_var_gt.setter
    @int_check(greater_than=-1)
    def int_var_gt(self, value):
        self._int_var_gt = value

    @property
    def int_var_lt(self):
        return self._int_var_lt

    @int_var_lt.setter
    @int_check(less_than=10)
    def int_var_lt(self, value):
        self._int_var_lt = value

    @property
    def not_none_var(self):
        return self._not_none_var

    @not_none_var.setter
    @not_none_check
    def not_none_var(self, value):
        self._not_none_var = value

    @property
    def int_not_none_var(self):
        return self._int_not_none_var

    @int_not_none_var.setter
    @int_check()
    @not_none_check
    def int_not_none_var(self, value):
        self._int_not_none_var = value

class TestTyper(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._bogus = Bogus()

    def test_bool_check_with_int(self):
        """Assign an integer to a bool.
        """
        with self.assertRaises(TypeError):
            self._bogus.bool_var = 0

    def test_bool_check_with_string(self):
        """Assign a string to a bool.
        """
        with self.assertRaises(TypeError):
            self._bogus.bool_var = 'string'

    def test_bool_check_with_none_type(self):
        """Assign a none type to a bool.
        """
        with self.assertRaises(TypeError):
            self._bogus.bool_var = None

    def test_bool_check_with_valid_assignment(self):
        """Assign a valid bool.
        """
        msg = 'Bool assignment should honor value and not raise exception'
        self._bogus.bool_var = False
        self.assertFalse(self._bogus.bool_var, msg)

        self._bogus.bool_var = True
        self.assertTrue(self._bogus.bool_var, msg)

    def test_int_check_with_bool(self):
        """Assign a bool to an int.
        """
        with self.assertRaises(TypeError):
            self._bogus.int_var = False

    def test_int_check_with_string(self):
        """Assign a string to an int.
        """
        with self.assertRaises(TypeError):
            self._bogus.int_var = 'string'

    def test_int_check_with_none_type(self):
        """Assign "None" type to an int.
        """
        self._bogus.int_var = None
        msg = 'Integer assignment should accept "None"'
        self.assertIsNone(self._bogus.int_var, msg)

    def test_int_check_with_valid_assignment(self):
        """Assign a valid int.
        """
        msg = 'Int assignment should honor value and not raise exception'
        self._bogus.int_var = 0
        self.assertFalse(self._bogus.int_var, msg)

    def test_int_check_with_valid_int_lower_than_range(self):
        """Assign a valid int which is lower than range.
        """
        with self.assertRaises(ValueError):
            self._bogus.int_var_gt = -1

    def test_int_check_with_valid_int_higher_than_range(self):
        """Assign a valid int which is higher than range.
        """
        with self.assertRaises(ValueError):
            self._bogus.int_var_lt = 11

    def test_not_none_check_with_none_value(self):
        """Assign a none value to a not-None variable.
        """
        with self.assertRaises(TypeError):
            self._bogus.not_none_var = None

    def test_not_none_check_with_int_value(self):
        """Assign an int value with a not_none check.
        """
        msg = 'Integer assignment around a not_none check should be honored'
        expected = random.randint(1, 10)
        self._bogus.not_none_var = expected
        self.assertEqual(self._bogus.not_none_var, expected, msg)

    def test_int_check_not_none_with_a_none_value(self):
        """Assign "None" to non-None integer.
        """
        with self.assertRaises(TypeError):
            self._bogus.int_not_none_var = None

    def test_int_check_not_none_with_a_int_value(self):
        """Assign an int to a not-None integer variable.
        """
        msg = 'Integer assignment around a not_none check should be honored'
        expected = random.randint(1, 10)
        self._bogus.int_not_none_var = expected
        self.assertEqual(self._bogus.int_not_none_var, expected, msg)

    @classmethod
    def tearDownClass(cls):
        cls._bogus = None
