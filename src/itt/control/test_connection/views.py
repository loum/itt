from django.http import HttpResponse
from django.template import (RequestContext,
                             loader)

from test_connection.models import TestConnection
from test_connection.forms import TestConnectionForm


def index(request):
    """
    """
    response = _index_get(request)

    return response


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
