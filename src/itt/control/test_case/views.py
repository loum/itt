from django.http import HttpResponse
from django.template import (RequestContext,
                             loader)

from test_case.models import TestCase
from test_case.forms import TestCaseForm

def index(request):
    """
    """
    response = _index_get(request)

    return response


def _index_get(request):
    """
    """
    test_case_list = TestCase.objects.all()
    t = loader.get_template('test_case/index.html')

    form = TestCaseForm()
    c = RequestContext(request,
                       {'form': form,
                        'test_case_list': test_case_list})

    return HttpResponse(t.render(c))
