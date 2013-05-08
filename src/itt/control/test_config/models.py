from django.db import models
from django.core.validators import MinValueValidator

from common.models import (CommonModel,
                           IntegerRangeField,
                           FloatRangeField)


class TestConfig(CommonModel):

    name = models.CharField(max_length=20,
                            unique=True)
    upload = models.BooleanField()
    bytes = IntegerRangeField(default=0,
                              min_value=0,
                              validators=[MinValueValidator(0)])
    minimum_gap = FloatRangeField(default=0,
                                  min_value=0,
                                  validators=[MinValueValidator(0)])
    chunk_size = IntegerRangeField(default=0,
                                   min_value=0,
                                   validators=[MinValueValidator(0)])
