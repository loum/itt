__all__ = [
    "bool_check",
]

def bool_check(f):
    """Bool property attribute checker.

    If you are using a property construct and want to ensure that the
    attribute is assigned *only* a ``bool`` then use this decorator.

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
