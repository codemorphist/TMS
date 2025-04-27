from django.db import models
from django.contrib.auth.models import AbstractUser


class PanelUser(AbstractUser):
    CLIENT = 'client'
    PROVIDER = 'provider'
    OPERATOR = 'operator'
    USER_TYPES = {
        CLIENT: 'Client',
        PROVIDER: 'Provider',
        OPERATOR: 'Operator',
    }

    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField()
    user_type = models.CharField(max_length=20,
                                 choices=USER_TYPES,
                                 default=OPERATOR)

    def __str__(self):
        return self.username