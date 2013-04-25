from django.forms import ModelForm

from server.models import Server

class ServerForm(ModelForm):
    class Meta:
        model = Server
        fields = ('name',
                  'protocol',
                  'port',
                  'root')
