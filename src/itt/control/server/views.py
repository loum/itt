from django.http import (HttpResponse,
                         HttpResponseRedirect)
from django.template import (Context,
                             RequestContext,
                             loader)

from server.models import Server
from server.forms import ServerForm

def index(request):
    """Display the current ITT server list.

    The ``index.html`` page is the :mod:`itt.control.server` entry point
    and is accessible bia::

        http://<hostname>:8080/server/

    Each ITT installation support the FTP, TFTP and HTTP server protocols.
    ITT can run a default instance of each server with preconfigured
    settings.  This screen presents the details around these defaults.

    """
    server_list = Server.objects.all()

    t = loader.get_template('server/index.html')
    c = RequestContext(request,
                       {'server_list': server_list,})

    return HttpResponse(t.render(c))

def insert(request):
    """Present a form that allows:

     * New server resources to be defined
     * Control server resources

    """
    response = None

    t = loader.get_template('server/server_form.html')

    if request.method =='POST':
        # Check for the Cancel button.
        if 'cancel' not in request.POST:
            form = ServerForm(request.POST)
            form.save()

        response = HttpResponseRedirect('/server/')
    else:
        form = ServerForm()
        c = RequestContext(request,
                        {'form': form,})
        response = HttpResponse(t.render(c))

    return response
