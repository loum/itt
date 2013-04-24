from django.db import models

class Config(models.Model):
    SLAVE = 'sl'
    MASTER = 'ma'
    ROLE_CHOICES = (
        (MASTER, 'Master'),
        (SLAVE, 'Slave'),
    )

    standalone = models.BooleanField()
    client = models.BooleanField()
    server = models.BooleanField()
    role = models.CharField(max_length=2,
                            choices=ROLE_CHOICES,
                            default=SLAVE)
