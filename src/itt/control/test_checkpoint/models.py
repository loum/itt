__all__ = [
    "Node",
    "Checkpoint",
]

from django.db import models


class Node(models.Model):
    """The Node model.

    """
    uid = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=50)


class Checkpoint(models.Model):
    """The Checkpoint model.

    """
    node = models.ForeignKey(Node)
    data = models.CharField(max_length=50)
    created_date = models.DateTimeField()
