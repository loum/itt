from django.template import (RequestContext,
                             loader)
from django.http import (HttpResponse,
                         HttpResponseRedirect)

from test_content.models import TestContent
from test_content.forms import TestContentForm
from common.utils import parse_pk


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
    status = HttpResponseRedirect('/testcontent/')

    try:
        if request.POST['submit']:
            pk = parse_pk(request.POST['submit'])

            if pk is not None:
                # Get the TestContent record and present in the edit form.
                instance = TestContent.objects.get(pk=pk)
                t = loader.get_template('test_content/update.html')

                data = dict(instance.get_fields())
                form = TestContentForm(initial=data)
                c = RequestContext(request,
                                   {'form': form})

                status = HttpResponse(t.render(c))
    except KeyError:
        pass

    return status


def _index_get(request):
    """
    """
    test_content_list = TestContent.objects.all()
    t = loader.get_template('test_content/index.html')

    form = TestContentForm()
    c = RequestContext(request,
                       {'form': form,
                        'test_content_list': test_content_list})

    return HttpResponse(t.render(c))


def _index_post(request):
    """
    """
    # Note: the 'cancel' submit will fall through to the return.
    try:
        if request.POST['submit']:
            form = None

            if request.POST['submit'] == 'Add Test Content':
                form = TestContentForm(request.POST)
            elif request.POST['submit'] == 'Update Test Content':
                instance = TestContent.objects.get(name=request.POST['name'])
                form = TestContentForm(request.POST, instance=instance)

            if form is not None:
                form.save()
    except KeyError:
        pass

    return HttpResponseRedirect('/testcontent/')
