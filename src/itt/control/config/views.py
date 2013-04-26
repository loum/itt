from django.http import (HttpResponse,
                         HttpResponseRedirect)
from django.template import (Context,
                             RequestContext,
                             loader)

from config.models import Config
from config.forms import ConfigForm

def index(request, config_id=1):
    """Display the current ITT installation settings.

    The ``index.html`` page as as the :mod:`itt.control.config` entry point
    and is accessible via::

        http://<hostname>:8080/config/

    Every ITT installation requires appropriate settings in order to
    perform its appropriate function on the network.  As such, the
    :mod:`itt.control.config` ``index.html`` will be one of the first
    screens required post-ITT install.

    """
    # Provide a quick view of the current ITT instance settings.
    config = Config.objects.get()

    t = loader.get_template('config/index.html')
    c = Context({
        'config': config,
    })

    return HttpResponse(t.render(c))

def update(request, config_id=1):
    """Present a form that allows the ITT instance configuration settings
    to be modified. 
    """
    response = None

    config = Config.objects.get(id=config_id)

    t = loader.get_template('config/config_form.html')

    if request.method == 'POST':
        # Check for the Cancel button.
        if 'cancel' not in request.POST:
            form = ConfigForm(request.POST, instance=config)
            form.save()

        response = HttpResponseRedirect('/config/')
    else:
        form = ConfigForm(instance=config)
        c = RequestContext(request,
                           {'form': form,
                            'config': config,})
        response = HttpResponse(t.render(c))

    return response
