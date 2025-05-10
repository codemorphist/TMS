from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import PanelUser

admin.site.register(PanelUser, UserAdmin)