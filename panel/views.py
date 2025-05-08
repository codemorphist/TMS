from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import FormView, UpdateView, DetailView, TemplateView
from django.views.generic.list import ListView

from users.utils import RoleBasedMixin


class ClientPanelView(TemplateView):
    template_name = 'panel/panel/client.html'


class ProviderPanelView(TemplateView):
    template_name = 'panel/panel/provider.html'


class OperatorPanelView(TemplateView):
    template_name = 'panel/panel/operator.html'


class PanelView(View, RoleBasedMixin):
    views = {
        'client': ClientPanelView,
        'provider': ProviderPanelView,
        'operator': OperatorPanelView,
    }
