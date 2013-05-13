__all__ = [
    "TestCase",
]

from django.db import models

from common.models import CommonModel
from control.test_config.models import TestConfig
from control.test_content.models import TestContent
from control.test_connection.models import TestConnection


class TestCase(CommonModel):
    """The TestCase Model.
    """
    name = models.CharField(max_length=20,
                            unique=True)
    test_configuration = models.ForeignKey(TestConfig)
    test_content = models.ForeignKey(TestContent)
    test_connection = models.ForeignKey(TestConnection)
