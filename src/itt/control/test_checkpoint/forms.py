from django.forms import ModelForm

from test_checkpoint.models import Checkpoint


class TestCheckpointForm(ModelForm):
    class Meta:
        model = Checkpoint
