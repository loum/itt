from django.db import models

import itt


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

    def status(self):
        server = itt.ServerConfig(server=self.protocol)
        daemon = getattr(*server.lookup)(**server.kwargs)

        return daemon.status()
