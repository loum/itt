from django.db import models


class Server(models.Model):
    FTP= 'ftp'
    TFTP= 'tftp'
    HTTP= 'http'
    PROTOCOL_CHOICES = (
        (FTP, 'FTP'),
        (TFTP, 'TFTP'),
        (HTTP, 'HTTP'),
    )

    protocol =  models.CharField(max_length=4,
                                 choices=PROTOCOL_CHOICES)
    port = models.IntegerField()
    root = models.CharField(max_length=100)
    name = models.CharField(max_length=20, unique=True)
    active = models.BooleanField(default=False)
