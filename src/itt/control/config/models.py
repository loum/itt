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

    def get_fields(self):
        """Sugar function that returns a list of tuples representing
        the key, value pair of the Config model object.

        Example usage::

        >>> from config.models import Config
        >>> config_list = Config.objects.all()
        >>> for config in config_list:
        ...     config.get_fields()
        ... 
        [('id', u'1'), ('standalone', u'True'), ('client', u'True'), ...]

        **Returns:**
            list of tuples representing the (key, value) pair of the
            Config model object.

        """
        return [(f.name,
                 f.value_to_string(self)) for f in Config._meta.fields]
