from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.views import View

from users.models import PanelUser


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

    __default_no_auth__ = 'users:login'

    def dispatch(self, request, *args, **kwargs):
        print('In dispatch')
        user = request.user

        if not user.is_authenticated:
            if self.no_auth is None:
                return redirect(self.__default_no_auth__)
            return self.no_auth(request, *args, **kwargs)

        if user.role not in self.views:
            if self.no_role is None:
                raise PermissionDenied()
            return self.no_role(request, *args, **kwargs)

        view = self.views[user.role]
        return view(request, *args, **kwargs)