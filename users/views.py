from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse

from users.forms import PanelUserCreationForm
from users.models import PanelUser
from users.utils import RegisterMixin


class PanelUserLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse('panel:panel')


class PanelUserLogoutView(LogoutView):
    next_page = 'users:login'


class RegisterPanelUser(RegisterMixin, CreateView):
    model = PanelUser
    form_class = PanelUserCreationForm
    template_name = 'users/register.html'
    user_type = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        match self.user_type:
            case PanelUser.CLIENT:
                title = 'Register Client'
            case PanelUser.PROVIDER:
                title = 'Register Provider'
            case _:
                raise TypeError('Invalid user type')
        context['title'] = title
        return context

    def get_success_url(self):
        return reverse('panel:panel')


class RegisterClient(RegisterPanelUser):
    user_type = PanelUser.CLIENT


class RegisterProvider(RegisterPanelUser):
    user_type = PanelUser.PROVIDER
