from django.http import (HttpResponse,
                         HttpResponseRedirect)
from django.template import (RequestContext,
                             loader)

from test_checkpoint.models import Checkpoint
from test_checkpoint.forms import TestCheckpointForm
import common.utils


def index(request):
    """
    """
    checkpoints = Checkpoint.objects.all()

    form = TestCheckpointForm()
    c = RequestContext(request,
                       {'form': form,
                        'test_checkpoint_list': checkpoints})

    t = loader.get_template('test_checkpoint/index.html')

    return HttpResponse(t.render(c))


def search(request):
    """
    """
    t = loader.get_template('test_checkpoint/search.html')
    form = TestCheckpointForm()
    c = RequestContext(request,
                        {'form': form})

    return HttpResponse(t.render(c))


def results(request):
    """
    """
    # Set a default response.
    response = HttpResponseRedirect('/testcheckpoint/search')

    if request.method == 'POST':
        # Check if we need to filter on the node UID.
        try:
            if request.POST['node']:
                node = request.POST['node']
                cp = Checkpoint.objects.filter(node=node)
            else:
                cp = Checkpoint.objects.all()

            form = TestCheckpointForm()
            c = RequestContext(request,
                            {'form': form,
                                'test_checkpoint_list': cp})

            t = loader.get_template('test_checkpoint/results.html')
            response = HttpResponse(t.render(c))
        except KeyError:
            pass

    return response


def delete(request):
    """
    """
    common.utils.delete(request, Checkpoint)

    return HttpResponseRedirect('/testcheckpoint/')
