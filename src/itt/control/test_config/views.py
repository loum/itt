from django.http import HttpResponse
from django.template import (RequestContext,
                             loader)

from test_config.models import TestConfig

def index(request):
    """
    """
    test_config_list = TestConfig.objects.all()

    response = None

    response = _index_get(request, test_config_list)

    return response

def _index_get(request, test_config_list):
    """
    """
    t = loader.get_template('test_config/index.html')

    c = RequestContext(request,
                       {'test_config_list': test_config_list,})

    return HttpResponse(t.render(c))
