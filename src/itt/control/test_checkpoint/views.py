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
    test_checkpoint_list = Checkpoint.objects.all()
    t = loader.get_template('test_checkpoint/index.html')

    form = TestCheckpointForm()
    c = RequestContext(request,
                       {'form': form,
                        'test_checkpoint_list': test_checkpoint_list})

    return HttpResponse(t.render(c))

def delete(request):
    """
    """
    common.utils.delete(request, Checkpoint)

    return HttpResponseRedirect('/testcheckpoint/')
