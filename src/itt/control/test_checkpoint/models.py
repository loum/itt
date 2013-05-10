__all__ = [
    "Node",
    "Checkpoint",
]

from django.db import models
from tastypie.utils.timezone import now


class Node(models.Model):
    """The Node model.

    """
    uid = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=50)


class Checkpoint(models.Model):
    """The Checkpoint model.

    """
    node = models.ForeignKey(Node)
    date = models.DateTimeField(default=now)
    data = models.CharField(max_length=50)
