from django.http import (HttpResponse,
                         HttpResponseRedirect)
from django.template import (RequestContext,
                             loader)

from test_case.models import TestCase
from test_case.forms import TestCaseForm
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
    response = HttpResponseRedirect('/testcase/')

    try:
        if request.POST['submit']:
            #  See if we can extract the primary key from the submit
            # input type's value.
            pk = common.utils.parse_pk(request.POST['submit'])

            if pk is not None:
                # Get the TestCase record and present in edit form.
                instance = TestCase.objects.get(pk=pk)
                t = loader.get_template('test_case/update.html')

                data = dict(instance.get_fields())
                form = TestCaseForm(initial=data)
                c = RequestContext(request,
                                   {'form': form})

                response = HttpResponse(t.render(c))
    except KeyError:
        pass

    return response


def _index_post(request):
    """
    """
    try:
        if request.POST['submit']:
            form = None

            if request.POST['submit'] == 'Add Test Case':
                form = TestCaseForm(request.POST)
            elif request.POST['submit'] == 'Update Test Case':
                instance = TestCase.objects.get(name=request.POST['name'])
                form = TestCaseForm(request.POST, instance=instance)

            if form is not None:
                form.save()

    except KeyError:
        pass

    return HttpResponseRedirect('/testcase/')


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
