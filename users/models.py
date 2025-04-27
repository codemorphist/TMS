from django.db import models
from django.contrib.auth.models import AbstractUser


class PanelUser(AbstractUser):
    USER_TYPES = {
        'client': 'Client',
        'provider': 'Provider',
        'operator': 'Operator',
    }

    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField()
    user_type = models.CharField(max_length=20,
                                 choices=USER_TYPES,
                                 default=USER_TYPES['client'])

    def __str__(self):
        return self.username