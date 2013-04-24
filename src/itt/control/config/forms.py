from django.forms import ModelForm

from config.models import Config

class ConfigForm(ModelForm):
    class Meta:
        model = Config
