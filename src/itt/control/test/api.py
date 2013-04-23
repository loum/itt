__all__ = [
    "NodeResource",
    "CheckpointResource"
]

from tastypie import fields
from tastypie.validation import Validation
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from test.models import (Node, Checkpoint)


class NodeResource(ModelResource):
    """
    """
    class Meta:
        queryset = Node.objects.all()
        resource_name = 'node' 
        authorization = Authorization()
        validation = Validation()

        always_return_data = True


class CheckpointResource(ModelResource):
    """The Checkpoint REST resource.

    """
    node = fields.ForeignKey(NodeResource, 'node')

    class Meta:
        queryset = Checkpoint.objects.all()
        resource_name = 'checkpoint'
        authorization = Authorization()

        always_return_data = True
