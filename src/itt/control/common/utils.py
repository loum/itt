__all__ = [
    "parse_pk",
    "delete",
]

import re


def parse_pk(input_value):
    """Tables in the :mod:`itt.control.test_config.views` use a input
    field value construct of the form <app>_<acton>_pk_<pk>.  For example::

        ...
        <input type="image"
               name="submit"
               value="test_config_del_pk_2"
               src="/static/images/itt_delete.png"
               alt="Test Config Delete"/ >
        ...

    This function is a helper to extract the primary key from the input
    type value option.  Example usage::

    **Args:**
        input_value (``str``): the value from which the primary key will be
        attempt to be extracted from.

    **Returns:**
        ``int`` primary key or ``None`` if extraction fails.

    """
    pk = None

    pk_re = re.compile('.*_pk_(\d+)$')

    try:
        pk = int(pk_re.match(input_value).group(1))
    except AttributeError:
        pass

    return pk


def delete(request, FormObject):
    """
    """
    try:
        if request.POST['submit']:
            # See if we can extract the primary key from the submit
            # input type's value.
            pk = parse_pk(request.POST['submit'])

            if pk is not None:
                instance = FormObject.objects.get(pk=pk)
                instance.delete()
    except KeyError:
        pass
