from django.http import (HttpResponse,
                         HttpResponseRedirect)
from django.template import (RequestContext,
                             loader)

import subprocess
from config.models import Config
from config.forms import ConfigForm
from server.models import Server

def index(request, config_id=1):
    """Present a form that allows the ITT instance configuration settings
    to be modified. 
    """
    config = Config.objects.get(id=config_id)

    if request.method == 'POST':
        response = _index_post(request, config)
    else:
        response = _index_get(request, config)

    return response

def _index_post(request, config):
    """
    """
    # Note: the 'cancel' submit will fall through to the return.
    # TODO: this is a bit fugly ...
    try:
        if request.POST['submit'] == 'Change Settings':
            form = ConfigForm(request.POST, instance=config)
            form.save()
        elif request.POST['submit'] == 'Start default FTP':
            _server_control('ftp', 'start')
        elif request.POST['submit'] == 'Stop default FTP':
            _server_control('ftp', 'stop')
        elif request.POST['submit'] == 'Start default TFTP':
            _server_control('tftp', 'start')
        elif request.POST['submit'] == 'Stop default TFTP':
            _server_control('tftp', 'stop')
        elif request.POST['submit'] == 'Start default HTTP':
            _server_control('http', 'start')
        elif request.POST['submit'] == 'Stop default HTTP':
            _server_control('http', 'stop')
    except KeyError:
        pass

    return HttpResponseRedirect('/config/')

def _index_get(request, config):
    """
    """
    server_list = Server.objects.all()
    t = loader.get_template('config/index.html')

    form = ConfigForm(instance=config)
    c = RequestContext(request,
                       {'form': form,
                       'config': config,
                       'server_list': server_list})

    return HttpResponse(t.render(c))

def _server_control(type, action):
    """
    """
    subprocess.call(['../server/bin/ittserverd.py', type, action],
                     close_fds=True)
