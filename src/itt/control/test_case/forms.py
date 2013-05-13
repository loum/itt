from django.forms import ModelForm

from test_case.models import TestCase


class TestCaseForm(ModelForm):
    class Meta:
        model = TestCase
