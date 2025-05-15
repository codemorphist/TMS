from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import F
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from users.models import Role
from users.utils import RoleBasedView, RoleRequiredMixin


class PanelView(RoleRequiredMixin, TemplateView):
    allowed_roles = [Role.CLIENT, Role.PROVIDER, Role.OPERATOR]
    template_name = 'panel/panel.html'


