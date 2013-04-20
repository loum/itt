from django.db import models
from tastypie.utils.timezone import now

class Checkpoint(models.Model):
    """The Checkpoint model.

    """
    date = models.DateTimeField(default=now)
    data = models.CharField(max_length=50)
