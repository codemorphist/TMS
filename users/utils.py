from pickletools import read_decimalnl_short
from typing import Callable

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View

from users.models import PanelUser, Role


class RegisterMixin:
    user_role = None


class AnonymousRequiredMixin:
    """
    Require that the user is authenticated, else reddirect
    """
    redirect_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class RoleRequiredMixin:
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        role = getattr(request.user, 'role', None)

        if not request.user.is_authenticated:
            return redirect('users:login')

        if role not in self.allowed_roles:
            raise PermissionDenied()

        return super().dispatch(request, *args, **kwargs)


class RoleBasedView(View):
    """
    Return View based on the user role

    Tips:
        * In `views` define role and View
          views = {
            'client': ClientView,
            ...
          }
        * no_auth View if user is not authenticated
        * no_role View if user.role not in views
    """
    views = {}
    no_auth = None
    no_role = None

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            if self.no_auth is None:
                raise PermissionDenied()
            return self.no_auth(request, *args, **kwargs)

        if user.role == Role.ADMIN:
            return redirect('admin:index')

        if user.role not in self.views:
            if self.no_role is None:
                raise PermissionDenied()
            return self.no_role(request, *args, **kwargs)

        view = self.views[user.role]
        return view(request, *args, **kwargs)
