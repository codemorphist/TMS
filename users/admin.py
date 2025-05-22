from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .forms import AdminPanelUserChangeForm, AdminPanelUserCreationForm
from .models import PanelUser

# Custom creation form

# Admin config
class PanelUserAdmin(UserAdmin):
    add_form = AdminPanelUserCreationForm
    form = AdminPanelUserChangeForm
    model = PanelUser

    list_display = ('username', 'full_name', 'email', 'role')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )

    add_fieldsets = (
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'email')}),
        ('Role', {'fields': ('role',)}),
        ('Password', {'fields': ('password1', 'password2')}),
    )

    def full_name(self, user):
        return f'{user.first_name} {user.last_name}'

admin.site.register(PanelUser, PanelUserAdmin)

