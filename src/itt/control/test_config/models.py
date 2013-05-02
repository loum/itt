from django.db import models
from django.core.validators import MinValueValidator


class IntegerRangeField(models.IntegerField):

    def __init__(self,
                 verbose_name=None,
                 name=None,
                 min_value=None,
                 max_value=None,
                 **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        models.IntegerField.__init__(self,
                                     verbose_name,
                                     name,
                                     **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value,
                    'max_value': self.max_value}
        defaults.update(kwargs)

        return super(IntegerRangeField, self).formfield(**defaults)


class FloatRangeField(models.FloatField):

    def __init__(self,
                 verbose_name=None,
                 name=None,
                 min_value=None,
                 max_value=None,
                 **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        models.FloatField.__init__(self,
                                   verbose_name,
                                   name,
                                   **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value,
                    'max_value': self.max_value}
        defaults.update(kwargs)

        return super(FloatRangeField, self).formfield(**defaults)


class TestConfig(models.Model):

    upload = models.BooleanField()
    bytes = IntegerRangeField(default=0,
                              min_value=0,
                              validators=[MinValueValidator(0)])
    minimum_gap = FloatRangeField(min_value=0,
                                  validators=[MinValueValidator(0)])

    def get_fields(self):
        """Sugar function that returns a list of tuples representing
        the key, value pair of the TestConfig model object.

        Example usage::

        >>> from test_config.models import TestConfig
        >>> test_config_list = TestConfig.objects.all()
        >>> for test_config in test_config_list:
        ...     test_config.get_fields()
        ...
        [('id', u'1'), ('upload', u'True') ...]

        **Returns:**
            list of tuples representing the (key, value) pair of the
            TestConfig model object.

        """
        return [(f.name,
                 f.value_to_string(self)) for f in TestConfig._meta.fields]
