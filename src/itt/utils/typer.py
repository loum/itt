__all__ = [
    "bool_check",
    "int_check",
    "not_none_check",
]

import types

def bool_check(f):
    """Boolean property attribute checker.

    Use this decorator if you are using a property construct and want to
    ensure that the attribute is assigned *only* a ``bool`` value.

    For example, apply the ``bool_check`` decorator in the place where you
    define your property setter::

        from itt.utils.typer import bool_check
        ...
        @property
        def bool_var(self):
            return self._bool_var

        @bool_var.setter
        @bool_check
        def bool_var(self, value):
            self._bool_var = value

    **Raises:**
        ``TypeError`` exception if the value assigned to the variable is not
        a `bool` type.

    """
    def wrapped(self, *args):
        if type(args[0]) is not bool:
            raise TypeError('expecting a bool value')

        return(f(self, *args))

    return wrapped

def int_check(greater_than=None,
              less_than=None):
    """Integer property attribute checker.

    .. note::

        By default, ``None`` values are accepted.  See the
        :func:`not_none_check` decorator if ``None``'s if otherwise.

    This *meta decorator* construct accepts *greater_than* and *less_than*
    arguments that form acceptable ranges in addition to the standard
    integer type check.

    For example, apply the ``int_check`` decorator in the place where you
    define your property setter::

        from itt.utils.typer import int_check
        ...

        @property
        def int_var(self):
            return self._int_var

        @int_var.setter
        @int_check(greater_than=-1, less_than=101)
        def int_var(self, value):
            self._int_var = value

    This check will also ensure that the integer value is between 0 and 100.

    If you simply want an integer check without range restrictions::

        ...
        @int_var.setter
        @int_check()
        def int_var(self, value):
            self._int_var = value
        ...

    **Kwargs:**
        greater_than (int): The lower boundary of range (inclusive)

        less_than (int): The upper boundary of range (inclusive)

    **Raises:**
        ``TypeError`` exception if the value assigned to the variable is not
        an ``int`` type.
        ``ValueError`` exception if the value assigned to the variable is
        not within the specified range.

    """
    def wrapped(f):
        def validate(self, *args):
            if args[0] is not None:
                if type(args[0]) is not int:
                    raise TypeError('expecting a int value')

                if greater_than is not None:
                    if args[0] <= greater_than:
                        raise ValueError('expecting a int value > %d' %
                                        greater_than)

                if less_than is not None:
                    if args[0] >= less_than:
                        raise ValueError('expecting a int value < %d' %
                                        less_than)

            return(f(self, *args))

        return validate

    return wrapped

def not_none_check(f):
    """Not ``None`` property attribute checker.

    Since the ``None`` type can be universally applied to all Python
    variable types, this decorator can be used to restrict ``None`` value
    assignment.

    For example, apply the ``not_none_check`` decorator in the place where
    you define your property setter::

        from itt.utils.typer import not_none_check
        ...

        @property
        def not_none_var(self):
            return self._not_none_var

        @not_none_var.setter
        @not_none_check
        def not_none_var(self, value):
            self._not_none_var = value

    Can be used to with other variable checks to ensure non-None,
    type specific assignment::

        ...
        @int_not_none_var.setter
        @int_check()
        @not_none_check
        def int_not_none_var(self, value):
            self._int_not_none_var = value
        ...

    **Raises:**
        ``TypeError`` exception if the value assigned to the variable is a
        ``None`` type.

    """
    def wrapped(self, *args):
        if type(args[0]) is types.NoneType:
            raise TypeError('"None" value not accepted')

        return f(self, *args)

    return wrapped
