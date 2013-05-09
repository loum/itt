from django.http import (HttpResponse,
                         HttpResponseRedirect)
from django.template import (RequestContext,
                             loader)

from test_connection.models import TestConnection
from test_connection.forms import TestConnectionForm
import common.utils


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
    status = HttpResponseRedirect('/testconnection/')

    try:
        if request.POST['submit']:
            # See if we can extract the primary key from the submit
            # input type's value.
            pk = common.utils.parse_pk(request.POST['submit'])

            if pk is not None:
                # Get the TestConnection record and present in edit form.
                instance = TestConnection.objects.get(pk=pk)
                t = loader.get_template('test_connection/update.html')

                data = dict(instance.get_fields())
                form = TestConnectionForm(initial=data)
                c = RequestContext(request,
                                   {'form': form})

                status = HttpResponse(t.render(c))
    except KeyError:
        pass

    return status


def _index_post(request):
    """
    """
    # Note: the 'cancel' submit will fall through to the return.
    try:
        if request.POST['submit']:
            form = None

            if request.POST['submit'] == 'Add Test Connection':
                form = TestConnectionForm(request.POST)
            elif request.POST['submit'] == 'Update Test Connection':
                name = request.POST['name']
                instance = TestConnection.objects.get(name=name)
                form = TestConnectionForm(request.POST, instance=instance)

            if form:
                form.save()
    except KeyError:
        pass

    return HttpResponseRedirect('/testconnection/')


def _index_get(request):
    """
    """
    test_connection_list = TestConnection.objects.all()
    t = loader.get_template('test_connection/index.html')

    form = TestConnectionForm()
    c = RequestContext(request,
                       {'form': form,
                        'test_connection_list': test_connection_list})

    return HttpResponse(t.render(c))
