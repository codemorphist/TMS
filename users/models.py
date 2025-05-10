from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    ADMIN = 'admin', _('Admin')
    OPERATOR = 'operator', _('Operator')
    PROVIDER = 'provider', _('Provider')
    CLIENT = 'client', _('Client')
    USER = 'user', _('User')


class PanelUser(AbstractUser):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField()
    role = models.CharField(choices=Role.choices, max_length=100, blank=False, null=False, default=Role.USER)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = Role.ADMIN
            self.is_staff = True
        elif self.role == Role.OPERATOR:
            self.is_staff = True
        else:
            self.is_staff = False

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username