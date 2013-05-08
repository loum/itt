from django.template import (RequestContext,
                             loader)
from django.http import (HttpResponse,
                         HttpResponseRedirect)

from test_content.models import TestContent
from test_content.forms import TestContentForm


def index(request):
    """
    """
    if request.method == 'POST':
        response = _index_post(request)
    else:
        response = _index_get(request)

    return response

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

            if request.POST['submit'] == 'Add Content':
                form = TestContentForm(request.POST)

            if form:
                form.save()
    except KeyError:
        pass

    return HttpResponseRedirect('/testcontent/')
