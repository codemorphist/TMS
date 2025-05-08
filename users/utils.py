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