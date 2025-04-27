from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, UpdateView, DetailView
from django.views.generic.list import ListView


def panel(request: HttpRequest) -> HttpResponse:
    """
    View for home page of panel
    """
    return render(request, 'panel/panel.html')

