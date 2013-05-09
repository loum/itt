from django.db import models

import itt
import common.utils


class Server(models.Model):
    protocol = models.CharField(max_length=4,
                                choices=common.utils.PROTOCOL_CHOICES)
    port = models.IntegerField()
    root = models.CharField(max_length=100)
    name = models.CharField(max_length=20, unique=True)
    active = models.BooleanField(default=False)

    def status(self):
        server = itt.ServerConfig(server=self.protocol)
        daemon = getattr(*server.lookup)(**server.kwargs)

        return daemon.status()
