from django.forms import ModelForm

from test_connection.models import TestConnection


class TestConnectionForm(ModelForm):
    class Meta:
        model = TestConnection
