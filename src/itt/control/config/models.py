from django.db import models

class Config(models.Model):
    SLAVE = 'sl'
    MASTER = 'ma'
    ROLE_CHOICES = (
        (MASTER, 'Master'),
        (SLAVE, 'Slave'),
    )

    standalone = models.NullBooleanField()
    client = models.NullBooleanField()
    server = models.NullBooleanField()
    role = models.CharField(max_length=2,
                            choices=ROLE_CHOICES,
                            default=SLAVE)
