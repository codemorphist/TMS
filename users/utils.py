from django.shortcuts import redirect

from users.models import PanelUser


class RegisterMixin:
    user_role = None


class AnonymousRequiredMixin:
    redirect_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class RoleBasedMixin:
    """
    Return View based on user role

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
    __default_no_role__ = 'users:login'

    def get(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            if self.no_auth is None:
                return redirect(self.__default_no_auth__)
            return self.no_auth.as_view()(request, *args, **kwargs)

        if user.role not in self.views:
            if self.no_role is None:
                return redirect(self.__default_no_role__)
            return self.no_role.as_view()(request, *args, **kwargs)

        view = self.views[user.role]
        return view.as_view()(request, *args, **kwargs)