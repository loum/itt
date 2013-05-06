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
        test_config_list = TestConfig.objects.all()
        response = _index_get(request, test_config_list)

    return response


def update(request):
    """
    """
    status = HttpResponseRedirect('/testconfig/')

    try:
        if request.POST['submit']:
            # Search for a primary key in the "submit" key value.
            m = re.match(r'test_config_edit_pk_(\d+)',
                            request.POST['submit'])
            if m:
                test_config_pk = m.group(1)

                # Get the TestConfig record and present in edit form.
                instance = TestConfig.objects.get(pk=test_config_pk)
                t = loader.get_template('test_config/update.html')

                data = dict(instance.get_fields())
                form = TestConfigForm(initial=data)
                c = RequestContext(request,
                                {'form': form})

                status = HttpResponse(t.render(c))
    except:
        pass

    return status


def _index_post(request):
    """
    """
    # Note: the 'cancel' submit will fall through to the return.
    try:
        if request.POST['submit']:
            if request.POST['submit'] == 'Add Test Configuration':
                form = TestConfigForm(request.POST)
            elif request.POST['submit'] == 'Update Test Configuration':
                instance = TestConfig.objects.get(name=request.POST['name'])
                form = TestConfigForm(request.POST, instance=instance)

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
