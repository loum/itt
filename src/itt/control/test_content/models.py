from django.db import models
from django.core.validators import MinValueValidator

from common.models import (CommonModel,
                           IntegerRangeField)


class TestContent(CommonModel):

    name = models.CharField(max_length=20,
                            unique=True,
                           )
    static = models.BooleanField()
    bytes = IntegerRangeField(default=0,
                              min_value=0,
                              validators=[MinValueValidator(0)],
                             )
