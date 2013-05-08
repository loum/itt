import re
from django.http import (HttpResponse,
                         HttpResponseRedirect)
from django.template import (RequestContext,
                             loader)

from test_config.models import TestConfig
from test_config.forms import TestConfigForm


def index(request):
    """
    """
    if request.method == 'POST':
        response = _index_post(request)
    else:
        response = _index_get(request)

    return response


def update(request):
    """
    """
    status = HttpResponseRedirect('/testconfig/')

    try:
        if request.POST['submit']:
            # See if we can extract the primary key from the submit
            # input type's value.
            pk = _parse_pk(request.POST['submit'])

            if pk is not None:
                # Get the TestConfig record and present in edit form.
                instance = TestConfig.objects.get(pk=pk)
                t = loader.get_template('test_config/update.html')

                data = dict(instance.get_fields())
                form = TestConfigForm(initial=data)
                c = RequestContext(request,
                                   {'form': form})

                status = HttpResponse(t.render(c))
    except KeyError:
        pass

    return status


def delete(request):
    """
    """
    try:
        if request.POST['submit']:
            # See if we can extract the primary key from the submit
            # input type's value.
            pk = _parse_pk(request.POST['submit'])

            if pk is not None:
                # Get the TestConfig record and present in edit form.
                instance = TestConfig.objects.get(pk=pk)
                instance.delete()
    except KeyError:
        pass

    return HttpResponseRedirect('/testconfig/')


def _index_post(request):
    """
    """
    # Note: the 'cancel' submit will fall through to the return.
    try:
        if request.POST['submit']:
            form = None

            if request.POST['submit'] == 'Add Test Configuration':
                form = TestConfigForm(request.POST)
            elif request.POST['submit'] == 'Update Test Configuration':
                instance = TestConfig.objects.get(name=request.POST['name'])
                form = TestConfigForm(request.POST, instance=instance)

            if form:
                form.save()
    except KeyError:
        pass

    return HttpResponseRedirect('/testconfig/')


def _index_get(request):
    """
    """
    test_config_list = TestConfig.objects.all()
    t = loader.get_template('test_config/index.html')

    form = TestConfigForm()
    c = RequestContext(request,
                       {'form': form,
                        'test_config_list': test_config_list})

    return HttpResponse(t.render(c))


def _parse_pk(input_value):
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
