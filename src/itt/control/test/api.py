from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from test.models import Checkpoint


class CheckpointResource(ModelResource):
    """The Checkpoint REST resource.

    """
    class Meta:
        queryset = Checkpoint.objects.all()
        resource_name = 'checkpoint'
        authorization = Authorization()

        always_return_data = True
