from django.forms import ModelForm

from test_config.models import TestConfig


class TestConfigForm(ModelForm):
    class Meta:
        model = TestConfig
