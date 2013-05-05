from django.http import (HttpResponse,
                         HttpResponseRedirect)
from django.template import (RequestContext,
                             loader)

from test_config.models import TestConfig
from test_config.forms import TestConfigForm


def index(request):
    """
    """
    test_config_list = TestConfig.objects.all()

    if request.method == 'POST':
        response = _index_post(request)
    else:
        response = _index_get(request, test_config_list)

    return response


def _index_post(request):
    """
    """
    # Note: the 'cancel' submit will fall through to the return.
    try:
        if request.POST['submit'] == 'Add Test Configuration':
            form = TestConfigForm(request.POST)
            form.save()
    except KeyError:
        pass

    return HttpResponseRedirect('/testconfig/')


def _index_get(request, test_config_list):
    """
    """
    t = loader.get_template('test_config/index.html')

    form = TestConfigForm()
    c = RequestContext(request,
                       {'form': form,
                        'test_config_list': test_config_list})

    return HttpResponse(t.render(c))
