from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import FormView, UpdateView, DetailView, TemplateView
from django.views.generic.list import ListView

from users.utils import RoleBasedView


class ClientPanelView(TemplateView):
    template_name = 'panel/panel/client.html'


class ProviderPanelView(TemplateView):
    template_name = 'panel/panel/provider.html'


class OperatorPanelView(TemplateView):
    template_name = 'panel/panel/operator.html'


class PanelView(RoleBasedView):
    views = {
        'client': ClientPanelView.as_view(),
        'provider': ProviderPanelView.as_view(),
        'operator': OperatorPanelView.as_view(),
    }
