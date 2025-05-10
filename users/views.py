from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from users.forms import PanelUserCreationForm
from users.models import PanelUser, Role
from users.utils import RegisterMixin, AnonymousRequiredMixin


class PanelUserLoginView(AnonymousRequiredMixin, LoginView):
    template_name = 'users/login.html'
    redirect_url = 'users:profile'

    def get_success_url(self):
        return reverse('panel:panel')


class PanelUserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'users:login'


class RegisterPanelUser(AnonymousRequiredMixin, RegisterMixin, CreateView):
    model = PanelUser
    form_class = PanelUserCreationForm
    template_name = 'users/register.html'
    user_group = None
    redirect_url = 'users:profile'

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.user_role not in Role.values:
            raise TypeError(f'Invalid user role: {self.user_role}')

        self.object.role = self.user_role
        self.object.save()

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = self.user_role.label
        return context

    def get_success_url(self):
        return reverse('panel:panel')


class RegisterClient(RegisterPanelUser):
    user_role = Role.CLIENT


class RegisterProvider(RegisterPanelUser):
    user_role = Role.PROVIDER


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
