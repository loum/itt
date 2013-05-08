from django.template import (RequestContext,
                             loader)
from django.http import HttpResponse

from test_content.models import TestContent
from test_content.forms import TestContentForm


def index(request):
    """
    """
    test_content_list = TestContent.objects.all()
    response = _index_get(request, test_content_list)

    return response

def _index_get(request, test_content_list):
    """
    """
    t = loader.get_template('test_content/index.html')

    form = TestContentForm()
    c = RequestContext(request,
                       {'form': form,
                        'test_content_list': test_content_list})

    return HttpResponse(t.render(c))
