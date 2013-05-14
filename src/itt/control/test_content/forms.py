from django.forms import ModelForm

from test_content.models import TestContent


class TestContentForm(ModelForm):
    class Meta:
        model = TestContent
