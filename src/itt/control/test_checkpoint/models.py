__all__ = [
    "Node",
    "Checkpoint",
]

from django.db import models
from common.models import CommonModel


class Node(CommonModel):
    """The Node model.

    """
    uid = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=50)

    def __unicode__(self):
        return self.uid


class Checkpoint(CommonModel):
    """The Checkpoint model.

    """
    node = models.ForeignKey(Node)
    data = models.CharField(max_length=50)
