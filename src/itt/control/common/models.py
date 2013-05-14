"""The :mod:`itt.control.common` module is a place to put common
information that can be accessed by other modules.
"""

__all__ = [
    "CommonModel",
]

from django.db import models


class CommonModel(models.Model):
    """Common ITT Control and Command model functionality.

    The :class:`CommonModel` has been defined abstract.

    .. note::

        Don't instantiate this model directly.  Instead, inherit from it
        in your own models.  Common fields and functionality will be added
        to those of the child class.

    .. warning::

        It is an error to have fields in the abstract base class with the
        same name as those in the child.
    """
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def get_fields(self):
        """Sugar function that returns a list of tuples representing
        the key, value pair of the model object that inherits from
        :mod:`control.common.models.CommonModel`.

        Example usage (assuming ``TestConfig`` inherits from
        ``CommonModel``::

            >>> from test_config.models import TestConfig
            >>> test_config_list = TestConfig.objects.all()
            >>> for test_config in test_config_list:
            ...     test_config.get_fields()
            ...
            {'id': u'1', 'upload': True, ...}

        .. note::

            The method will honor Python's ``bool`` values.  For example,
            a value string "False" will represent ``bool`` ``False``.

        **Returns:**
            ``dict`` object representing the TestConfig model object's
            name, value pair.

        """
        d = dict((f.name,
                  f.value_to_string(self)) for f in self._meta.fields)

        for key in d:
            if d[key] == 'False' or d[key] == 'True':
                d[key] = d[key] == 'True'

        return d


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
