from django.http import (HttpResponse,
                         HttpResponseRedirect)
from django.template import (RequestContext,
                             loader)

from test_connection.models import TestConnection
from test_connection.forms import TestConnectionForm


def index(request):
    """
    """
    if request.method == 'POST':
       response = _index_post(request)
    else:
       response = _index_get(request)

    return response


def _index_post(request):
    """
    """
    # Note: the 'cancel' submit will fall through to the return.
    try:
        if request.POST['submit']:
            form = None

            if request.POST['submit'] == 'Add Test Connection':
                form = TestConnectionForm(request.POST)

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
