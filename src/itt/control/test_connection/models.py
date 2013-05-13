from django.db import models
from django.core.validators import (MinValueValidator,
                                     MaxValueValidator)

from common.models import (CommonModel,
                           IntegerRangeField)
import common.utils


class TestConnection(CommonModel):

    name = models.CharField(max_length=20,
                            unique=True)
    host = models.CharField(max_length=50)
    port = IntegerRangeField(min_value=1,
                             max_value=65535,
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(65535)])
    protocol = models.CharField(max_length=4,
                                choices=common.utils.PROTOCOL_CHOICES)

    def __unicode__(self):
        return self.name
